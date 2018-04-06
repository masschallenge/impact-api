from collections import (
    defaultdict,
    Counter,
    OrderedDict,
)

from accelerator.models import (
    Application,
    ExpertCategory,
    ExpertProfile,
    Industry,
    JudgeApplicationFeedback,
    JUDGING_FEEDBACK_STATUS_COMPLETE,
)

class AllocationAnalyzer(object):
    def __init__(self, judging_round):
        self.judging_round = judging_round
        self.jafs = JudgeApplicationFeedback.objects.feedbacks_for_round(judging_round)        
        self.apps = Application.objects.filter(
            judgeapplicationfeedback__in=self.jafs).distinct()

        self.app_stats = defaultdict(dict)
        self.stats = OrderedDict()

    def calc_all_stats(self):
        self.calc_completed_read_counts()
        self.calc_industry_distributions()
        self.calc_home_program_data()
        self.calc_gender_distributions()
        self.calc_expert_category_distribution()

    def calc_expert_category_distribution(self):

        read_by_category = defaultdict(int)
        read_by_more_than_one_of_category = defaultdict(int)
        not_read_by_category = defaultdict(int)

        categories = ExpertCategory.objects.all()
        for app in self.apps:
            for category in categories:
                cat_count = self.jafs.filter(
                    application=app,
                    feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE,
                    judge__expertprofile__expert_category=category).count()
                self.app_stats[app.id][category.name] = cat_count
                if cat_count > 0:
                    read_by_category[category.name] += 1
                if cat_count > 1:
                    read_by_more_than_one_of_category[category.name] += 1

                if cat_count == 0:
                    not_read_by_category[category.name] += 1
        self.stats.update({"Applications read by %ss" % cat.name: read_by_category[cat.name]
                           for cat in categories})
        self.stats.update({"Applications read by more than one %ss" % cat.name: read_by_more_than_one_of_category[cat.name]
                           for cat in categories})

        self.stats.update({"Applications not read by %ss" % cat.name: not_read_by_category[cat.name]
                           for cat in categories})
        for category in categories:
            self.stats['Total reads by %ss' % category.name] = self.jafs.filter(
                feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE,
                judge__expertprofile__expert_category=category).count()

    def calc_completed_read_counts(self):
        completed_reads = self.jafs.filter(
            feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE)
        self.read_counter = Counter([jaf.application_id for jaf in completed_reads])

        for app_id, read_count in self.read_counter.items():
            self.app_stats[app_id]['completed_reads'] = read_count
        self.stats['Total completed reads'] = completed_reads.count()
        self.stats['Average number of completed reads'] = (
            float(completed_reads.count())/self.apps.count())
        self.read_count_distribution = Counter(self.read_counter.values())

    def calc_industry_distributions(self):
        expert_industries = dict(ExpertProfile.objects.filter(
            user__judgeapplicationfeedback__in=self.jafs).distinct().values_list(
                'id', 'primary_industry'))
        top_level_industries = dict(Industry.objects.all().values_list(
            'pk', 'parent_id'))
        for pk, parent_id in top_level_industries.items():
            if parent_id is None:
                top_level_industries[pk]=pk

        apps_with_primary_industry_reader = []
        apps_missing_primary_industry_reader = defaultdict(int)
        apps_with_knowledgeable_reader = []
        apps_without_knowledgeable_reader = []

        for app in self.apps:
            industry = parent_industry(app.startup.primary_industry)
            app_expert_ids = self.jafs.filter(
                feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE,
                application=app).values_list('judge__expertprofile__id',
                                             flat=True)
            app_expert_industries = [top_level_industries[expert_industries[id]]
                                     for id in app_expert_ids]
            if industry.pk in app_expert_industries:
                apps_with_primary_industry_reader.append(app)
                apps_with_knowledgeable_reader.append(app)
            else:
                apps_missing_primary_industry_reader['total'] += 1
                apps_missing_primary_industry_reader[industry.name] += 1
                app_sibling_industries = [val for key, val in top_level_industries.items()
                                          if key == industry.pk]
                if self.jafs.filter(
                        feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE,
                        judge__expertprofile__additional_industries__in=app_sibling_industries,
                        application=app).exists():
                    apps_with_knowledgeable_reader.append(app)
                else:
                    apps_without_knowledgeable_reader.append(app)
        self.stats['Primary industry reader requirement satisfied'] = len(
            apps_with_primary_industry_reader)
        self.stats.update(
            {'Primary industry reader requirement unsatisfied: %s' % industry :app_count
             for industry, app_count in apps_missing_primary_industry_reader.items()})

        self.stats['Apps with at least one knowledgeable reader'] = len(
            apps_with_knowledgeable_reader)
        self.stats['Apps without at least one knowledgeable reader'] = len(
            apps_without_knowledgeable_reader)
        for industry in Industry.objects.filter(parent__isnull=True):
            self.stats['Total completed reads for %s' % industry.name] = self.jafs.filter(
                judge__expertprofile__primary_industry=industry,
                feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE).count()
            industry_startups = (
                self.apps.filter(startup__primary_industry=industry).count() +
                self.apps.filter(startup__primary_industry__parent=industry).count())

            self.stats['Total startups with primary industry %s' % industry.name] = industry_startups

    def calc_gender_distributions(self):
        total_female_reads = 0
        for app in self.apps:
            female_reads = self.jafs.filter(
                application=app,
                feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE,
                judge__expertprofile__gender='f').count()
            self.app_stats[app.id]['female_reads'] = female_reads
            total_female_reads += female_reads
        self.stats['Total reads by female judges'] = total_female_reads
        self.stats['Average reads by female judges'] = float(total_female_reads)/self.apps.count()

        no_female_reads = sum([1 for row in self.app_stats.values() if row['female_reads']==0])
        one_female_read = sum([1 for row in self.app_stats.values() if row['female_reads']==1])
        multi_female_reads = sum([1 for row in self.app_stats.values() if row['female_reads']>1])
        self.stats['Number of applications with no female judge reads'] = no_female_reads
        self.stats['Number of applications with exactly one female judge read'] = one_female_read
        self.stats['Number of applications with >1 female judge reads'] = multi_female_reads


    def calc_home_program_data(self):
        preferred_programs = {}
        program_counts = {}
        cycle = self.judging_round.program.cycle
        for app in self.apps:
            spi = app.startup.startupprograminterest_set.filter(
                applying=True, program__cycle=cycle).order_by('order').first()
            if spi:

                preferred_programs[app.id] = spi.program
                program_counts[spi.program] = 1 + program_counts.get(spi.program, 0)
            else:
                # how did this happen?
                pass
                
        hits = 0
        misses = 0
        program_misses = {}
        for app in self.apps:
            if app.id  in preferred_programs:
                program = preferred_programs[app.id]
                judges = self.jafs.filter(
                    feedback_status="COMPLETE",
                    application=app,
                    judge__expertprofile__home_program_family=program.program_family)
                if judges.count() == 0:
                    program_misses[program] = 1 + program_misses.get(program, 0)
                    misses += 1
                else:
                    hits += 1
        self.stats['Apps judged by at least one judge from their home program'] = hits
        self.stats['Apps not judged by any judge from their home program'] = misses
        for program in program_misses.keys():
            self.stats['%s apps not judged by any judge from that program' % program.name] = program_misses[program]
            
            total_program_reads = self.jafs.filter(
                feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE,
                judge__expertprofile__home_program_family=program.program_family)
            self.stats['Total apps for %s' % program.name] = program_counts[program]
            self.stats['Total reads for %s' % program.name] = total_program_reads.count()


    def calc_judge_bias_distribution(self):
        pass
        # judge_z_scores = {row['Judge ID']: row['Z-score'] for row in self.pivot_table.rows}
        # app_z_scores = defaultdict(list)
        # for app_id, judge_id in self.jafs.filter(
        #         feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE
        # ).values_list("application_id", "judge_id"):
        #     app_z_scores[app_id].append(judge_z_scores[judge_id])
        # for app_id, scores in app_z_scores.items():
        #     self.app_stats[app_id]['average_z_score'] = mean(scores)
        # average_of_z_scores = [row['average_z_score'] for row in self.app_stats.values()]
        # self.stats['Average average z-score'] = mean(average_of_z_scores)
        # self.stats['Max average z-score'] = max(average_of_z_scores)
        # self.stats['Min average z-score'] = min(average_of_z_scores)
        # self.stats['Number of apps with positive average z-score'] = len(
        #     [score for score in average_of_z_scores if score > 0])
        # self.stats['Number of apps with negative average z-score'] = len(
        #     [score for score in average_of_z_scores if score < 0])
        # self.stats['Number of apps with average z-score > .5'] = len(
        #     [score for score in average_of_z_scores if score > .5])
        # self.stats['Number of apps with average z-score < -.5'] = len(
        #     [score for score in average_of_z_scores if score < -.5])

        # self.stats['Max judge z-score for this round'] = max(judge_z_scores.values())
        # self.stats['Min judge z-score for this round'] = min(judge_z_scores.values())



def parent_industry(industry):
    return industry.parent or industry

def mean(collection):
    return float(sum(collection)) / len(collection)
