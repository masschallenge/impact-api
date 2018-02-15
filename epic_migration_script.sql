/*

pre:
setup mcproject+impact to share a DB

in mcproject:

git checkout AC-5039
git pull
vagrant ssh
cd /vagrant
sudo rm -rf src/django-accelerator/
sudo bin/buildout
find mcproject -name '*.pyc' | xargs rm

in impact:
git checkout AC-5039
git pull
make clean;make build;make dev;

in mcproject:
resetremotedb


in impact:
make bash
./manage.py migrate simpleuser 0002 --fake (mcproject runs it)
run fake migrations:
./manage.py migrate pdt 0002 --fake
./manage.py migrate
./manage.py dbshell
 */

-- un-apply deleted migrations
DELETE
FROM `django_migrations`
WHERE (`django_migrations`.`app` = 'accelerator'
       AND NOT (`django_migrations`.`id` = 179));

DELETE
FROM `django_migrations`
WHERE `django_migrations`.`app` IN ('mc', 'impact');

-- delete content types for accelerator models that are later "recreated"
DELETE
FROM `auth_user_user_permissions`
WHERE `auth_user_user_permissions`.`permission_id` IN (480,
                                                       481,
                                                       482,
                                                       483,
                                                       484,
                                                       485,
                                                       486,
                                                       472,
                                                       473,
                                                       474,
                                                       475,
                                                       476,
                                                       477,
                                                       478,
                                                       479);
DELETE
FROM `auth_group_permissions`
WHERE `auth_group_permissions`.`permission_id` IN (480,
                                                   481,
                                                   482,
                                                   483,
                                                   484,
                                                   485,
                                                   486,
                                                   472,
                                                   473,
                                                   474,
                                                   475,
                                                   476,
                                                   477,
                                                   478,
                                                   479);
DELETE
FROM `auth_permission`
WHERE `auth_permission`.`id` IN (480,
                                 481,
                                 482,
                                 483,
                                 484,
                                 485,
                                 486,
                                 472,
                                 473,
                                 474,
                                 475,
                                 476,
                                 477,
                                 478,
                                 479);
DELETE
FROM `django_content_type`
WHERE `django_content_type`.`id` IN (128,
                                     129,
                                     130,
                                     131,
                                     132);
-- delete unused accelerator tables

DROP TABLE accelerator_jobposting;
DROP TABLE accelerator_startup_recommendation_tags;
DROP TABLE accelerator_recommendationtag;
DROP TABLE accelerator_startup_related_industry;
DROP TABLE accelerator_startup;
DROP TABLE accelerator_organization;
DROP TABLE accelerator_industry;

-- rename mc content types to accelerator
UPDATE `django_content_type`
SET `app_label` = 'accelerator'
WHERE `django_content_type`.`app_label` = 'mc';

-- rename mc tables to accelerator
RENAME TABLE
    mc_application TO accelerator_application,
    mc_applicationanswer TO accelerator_applicationanswer,
    mc_applicationpanelassignment TO accelerator_applicationpanelassignment,
    mc_applicationquestion TO accelerator_applicationquestion,
    mc_applicationtype TO accelerator_applicationtype,
    mc_baseprofile TO accelerator_baseprofile,
    mc_country TO accelerator_country,
    mc_entrepreneurprofile TO accelerator_entrepreneurprofile,
    mc_entrepreneurprofile_interest_categories TO accelerator_entrepreneurprofile_interest_categories,
    mc_entrepreneurprofile_program_families TO accelerator_entrepreneurprofile_program_families,
    mc_entrepreneurprofile_recommendation_tags TO accelerator_entrepreneurprofile_recommendation_tags,
    mc_expert_related_industry TO accelerator_expert_related_industry,
    mc_expert_related_mentoringspecialty TO accelerator_expert_related_mentoringspecialty,
    mc_expertcategory TO accelerator_expertcategory,
    mc_expertinterest TO accelerator_expertinterest,
    mc_expertinteresttype TO accelerator_expertinteresttype,
    mc_expertprofile TO accelerator_expertprofile,
    mc_expertprofile_functional_expertise TO accelerator_expertprofile_functional_expertise,
    mc_expertprofile_interest_categories TO accelerator_expertprofile_interest_categories,
    mc_expertprofile_program_families TO accelerator_expertprofile_program_families,
    mc_expertprofile_recommendation_tags TO accelerator_expertprofile_recommendation_tags,
    mc_functionalexpertise TO accelerator_functionalexpertise,
    mc_industry TO accelerator_industry,
    mc_interestcategory TO accelerator_interestcategory,
    mc_jobposting TO accelerator_jobposting,
    mc_judgeapplicationfeedback TO accelerator_judgeapplicationfeedback,
    mc_judgeavailability TO accelerator_judgeavailability,
    mc_judgefeedbackcomponent TO accelerator_judgefeedbackcomponent,
    mc_judgepanelassignment TO accelerator_judgepanelassignment,
    mc_judgeroundcommitment TO accelerator_judgeroundcommitment,
    mc_judgingform TO accelerator_judgingform,
    mc_judgingformelement TO accelerator_judgingformelement,
    mc_judginground TO accelerator_judginground,
    mc_memberprofile TO accelerator_memberprofile,
    mc_memberprofile_interest_categories TO accelerator_memberprofile_interest_categories,
    mc_memberprofile_program_families TO accelerator_memberprofile_program_families,
    mc_memberprofile_recommendation_tags TO accelerator_memberprofile_recommendation_tags,
    mc_mentoringspecialties TO accelerator_mentoringspecialties,
    mc_mentorprogramofficehour TO accelerator_mentorprogramofficehour,
    mc_namedgroup TO accelerator_namedgroup,
    mc_newsletter TO accelerator_newsletter,
    mc_newsletter_recipient_roles TO accelerator_newsletter_recipient_roles,
    mc_newsletterreceipt TO accelerator_newsletterreceipt,
    mc_nodepublishedfor TO accelerator_nodepublishedfor,
    mc_observer TO accelerator_observer,
    mc_observer_newsletter_cc_roles TO accelerator_observer_newsletter_cc_roles,
    mc_panel TO accelerator_panel,
    mc_panel_sequence_updates TO accelerator_panel_sequence_updates,
    mc_panellocation TO accelerator_panellocation,
    mc_paneltime TO accelerator_paneltime,
    mc_paneltype TO accelerator_paneltype,
    mc_partner TO accelerator_partner,
    mc_partnerteammember TO accelerator_partnerteammember,
    mc_paypalpayment TO accelerator_paypalpayment,
    mc_paypalrefund TO accelerator_paypalrefund,
    mc_program TO accelerator_program,
    mc_programcycle TO accelerator_programcycle,
    mc_programfamily TO accelerator_programfamily,
    mc_programoverride TO accelerator_programoverride,
    mc_programpartner TO accelerator_programpartner,
    mc_programpartnertype TO accelerator_programpartnertype,
    mc_programrole TO accelerator_programrole,
    mc_programrolegrant TO accelerator_programrolegrant,
    mc_programstartupattribute TO accelerator_programstartupattribute,
    mc_programstartupstatus TO accelerator_programstartupstatus,
    mc_question TO accelerator_question,
    mc_recommendationtag TO accelerator_recommendationtag,
    mc_reference TO accelerator_reference,
    mc_refundcode TO accelerator_refundcode,
    mc_refundcode_programs TO accelerator_refundcode_programs,
    mc_refundcoderedemption TO accelerator_refundcoderedemption,
    mc_scenario TO accelerator_scenario,
    mc_scenarioapplication TO accelerator_scenarioapplication,
    mc_scenariojudge TO accelerator_scenariojudge,
    mc_scenariopreference TO accelerator_scenariopreference,
    mc_section TO accelerator_section,
    mc_section_interest_categories TO accelerator_section_interest_categories,
    mc_site TO accelerator_site,
    mc_siteprogramauthorization TO accelerator_siteprogramauthorization,
    mc_startup TO accelerator_startup,
    mc_startup_recommendation_tags TO accelerator_startup_recommendation_tags,
    mc_startup_related_industry TO accelerator_startup_related_industry,
    mc_startupattribute TO accelerator_startupattribute,
    mc_startupcycleinterest TO accelerator_startupcycleinterest,
    mc_startuplabel TO accelerator_startuplabel,
    mc_startuplabel_startups TO accelerator_startuplabel_startups,
    mc_startupmentorrelationship TO accelerator_startupmentorrelationship,
    mc_startupmentortrackingrecord TO accelerator_startupmentortrackingrecord,
    mc_startupoverridegrant TO accelerator_startupoverridegrant,
    mc_startupprograminterest TO accelerator_startupprograminterest,
    mc_startuprole TO accelerator_startuprole,
    mc_startupstatus TO accelerator_startupstatus,
    mc_startupteammember TO accelerator_startupteammember,
    mc_startupteammember_recommendation_tags TO accelerator_startupteammember_recommendation_tags,
    mc_us_state TO accelerator_us_state,
    mc_userlabel TO accelerator_userlabel,
    mc_userlabel_users TO accelerator_userlabel_users,
    mc_userrole TO accelerator_userrole,
    mc_bucketstate TO accelerator_bucketstate,
    mc_clearance TO accelerator_clearance,
    mc_judgeapplicationfeedback_viewers TO accelerator_judgeapplicationfeedback_viewers,
    mc_judgeroundcommitment_snapshot_apr13 TO accelerator_judgeroundcommitment_snapshot_apr13,
    mc_judgeroundcommitment_snapshot_apr6 TO accelerator_judgeroundcommitment_snapshot_apr6,
    mc_modelchange TO accelerator_modelchange,
    mc_organization TO accelerator_organization,
    pagetype_mc_categoryheaderpage TO pagetype_accelerator_categoryheaderpage,
    pagetype_mc_filepage TO pagetype_accelerator_filepage,
    pagetype_mc_siteredirectpage TO pagetype_accelerator_siteredirectpage,
    pagetype_mc_userrolemenu TO pagetype_accelerator_userrolemenu;

-- add
ALTER TABLE `mc_dev`.`accelerator_industry`
  ADD COLUMN created_at datetime NULL AFTER parent_id,
  ADD COLUMN updated_at datetime NULL;

ALTER TABLE `mc_dev`.`accelerator_functionalexpertise`
  ADD COLUMN created_at datetime NULL AFTER parent_id,
  ADD COLUMN updated_at datetime NULL;

-- drop foreign key constraints

ALTER TABLE accelerator_application DROP FOREIGN KEY application_type_id_refs_id_1ae6bcbb8b7a51f7;
ALTER TABLE accelerator_application DROP FOREIGN KEY mc_application_cycle_id_342a9e243209c5ac_fk_mc_programcycle_id;
ALTER TABLE accelerator_application DROP FOREIGN KEY startup_id_refs_id_7fcfeb6274a2cf06;
ALTER TABLE accelerator_applicationanswer DROP FOREIGN KEY application_id_refs_id_411fee7c8714c26b;
ALTER TABLE accelerator_applicationanswer DROP FOREIGN KEY application_question_id_refs_id_a46a5e5cf89082b;
ALTER TABLE accelerator_applicationpanelassignment DROP FOREIGN KEY application_id_refs_id_5152b4fd16cbc6e7;
ALTER TABLE accelerator_applicationpanelassignment DROP FOREIGN KEY panel_id_refs_id_6789f726de3f20a3;
ALTER TABLE accelerator_applicationpanelassignment DROP FOREIGN KEY scenario_id_refs_id_3a06b9ce88a7ff48;
ALTER TABLE accelerator_applicationquestion DROP FOREIGN KEY application_type_id_refs_id_3bdb0225e3315b49;
ALTER TABLE accelerator_applicationquestion DROP FOREIGN KEY mc_applicationque_question_id_7ef50c4fd6d26ced_fk_mc_question_id;
ALTER TABLE accelerator_applicationquestion DROP FOREIGN KEY mc_applicationquest_program_id_66498e7f19a549c0_fk_mc_program_id;
ALTER TABLE accelerator_applicationtype DROP FOREIGN KEY mc_ap_submission_label_id_2abe624624af233c_fk_mc_startuplabel_id;
ALTER TABLE accelerator_baseprofile DROP FOREIGN KEY user_id_refs_id_1d847b571bf4a42f;
ALTER TABLE accelerator_bucketstate DROP FOREIGN KEY mc_bucketstate_cycle_id_48a9f2e6a10a0b57_fk_mc_programcycle_id;
ALTER TABLE accelerator_bucketstate DROP FOREIGN KEY mc_buckets_program_role_id_4d187fafc6f72c1b_fk_mc_programrole_id;
ALTER TABLE accelerator_clearance DROP FOREIGN KEY mc_clearance_user_id_56b1ef565dac42f0_fk_auth_user_id;
ALTER TABLE accelerator_clearance DROP FOREIGN KEY mc_cle_program_family_id_1121ea2a0e27cb3c_fk_mc_programfamily_id;
ALTER TABLE accelerator_entrepreneurprofile DROP FOREIGN KEY current_program_id_refs_id_2803c3595327da1f;
ALTER TABLE accelerator_entrepreneurprofile DROP FOREIGN KEY user_id_refs_id_53baf31ff845a553;
ALTER TABLE accelerator_entrepreneurprofile_interest_categories DROP FOREIGN KEY a07f6664492cc0cba93055647e445144;
ALTER TABLE accelerator_entrepreneurprofile_interest_categories DROP FOREIGN KEY m_interestcategory_id_2f9bce490cc7e7d1_fk_mc_interestcategory_id;
ALTER TABLE accelerator_entrepreneurprofile_program_families DROP FOREIGN KEY D9f96e023f330f1daf1afb9f5777eb27;
ALTER TABLE accelerator_entrepreneurprofile_program_families DROP FOREIGN KEY mc_entr_programfamily_id_77da24e7f7fe1da3_fk_mc_programfamily_id;
ALTER TABLE accelerator_entrepreneurprofile_recommendation_tags DROP FOREIGN KEY D5013c86b0f9f94ffad092bd1b672724;
ALTER TABLE accelerator_entrepreneurprofile_recommendation_tags DROP FOREIGN KEY b5810e72efd01d2bff8625c14ee09bbb;

ALTER TABLE accelerator_expert_related_mentoringspecialty DROP FOREIGN KEY expertprofile_id_refs_id_3f465ca18c84b72c;
ALTER TABLE accelerator_expert_related_mentoringspecialty DROP FOREIGN KEY mentoringspecialties_id_refs_id_3f8513d1ac2a54bd;
ALTER TABLE accelerator_expertinterest DROP FOREIGN KEY interest_type_id_refs_id_5e5522cc50fd83bf;
ALTER TABLE accelerator_expertinterest DROP FOREIGN KEY program_family_id_refs_id_1f6adf119f933ad4;
ALTER TABLE accelerator_expertinterest DROP FOREIGN KEY user_id_refs_id_7d07b2a174293620;
ALTER TABLE accelerator_expertprofile DROP FOREIGN KEY current_program_id_refs_id_422bf68180f07688;
ALTER TABLE accelerator_expertprofile DROP FOREIGN KEY expert_category_id_refs_id_5e81f405336eabf7;
ALTER TABLE accelerator_expertprofile DROP FOREIGN KEY m_home_program_family_id_7195f1d6c310c128_fk_mc_programfamily_id;
ALTER TABLE accelerator_expertprofile DROP FOREIGN KEY user_id_refs_id_40501eb44c4c9fa;
ALTER TABLE accelerator_expertprofile_functional_expertise DROP FOREIGN KEY D0b7eb046846dfad308c321671208e09;
ALTER TABLE accelerator_expertprofile_functional_expertise DROP FOREIGN KEY mc_exper_expertprofile_id_422537af22076b9_fk_mc_expertprofile_id;
ALTER TABLE accelerator_expertprofile_interest_categories DROP FOREIGN KEY m_interestcategory_id_6ef95b1ffae507ce_fk_mc_interestcategory_id;
ALTER TABLE accelerator_expertprofile_interest_categories DROP FOREIGN KEY mc_exper_expertprofile_id_7e00099e73a0332_fk_mc_expertprofile_id;
ALTER TABLE accelerator_expertprofile_program_families DROP FOREIGN KEY mc_expe_programfamily_id_6fc0dc82fe2259c8_fk_mc_programfamily_id;
ALTER TABLE accelerator_expertprofile_program_families DROP FOREIGN KEY mc_exper_expertprofile_id_196e5da0e05f867_fk_mc_expertprofile_id;
ALTER TABLE accelerator_expertprofile_recommendation_tags DROP FOREIGN KEY D84638728bd07d6132d58b970de36bb8;
ALTER TABLE accelerator_expertprofile_recommendation_tags DROP FOREIGN KEY mc_expe_expertprofile_id_592fae483003d2c8_fk_mc_expertprofile_id;
ALTER TABLE accelerator_functionalexpertise DROP FOREIGN KEY parent_id_refs_id_868974a5;
ALTER TABLE accelerator_industry DROP FOREIGN KEY parent_id_refs_id_6ed29eaa37008679;
ALTER TABLE accelerator_interestcategory DROP FOREIGN KEY program_id_refs_id_15d5dfa7cd996b28;
ALTER TABLE accelerator_jobposting DROP FOREIGN KEY startup_id_refs_id_1f83d97ae8b1396c;
ALTER TABLE accelerator_judgeapplicationfeedback DROP FOREIGN KEY application_id_refs_id_7e82e59f3ba4b370;
ALTER TABLE accelerator_judgeapplicationfeedback DROP FOREIGN KEY form_type_id_refs_id_7492120ae35e1848;
ALTER TABLE accelerator_judgeapplicationfeedback DROP FOREIGN KEY judge_id_refs_id_21504b8905ba9b3c;
ALTER TABLE accelerator_judgeapplicationfeedback DROP FOREIGN KEY panel_id_refs_id_56a7c73b7764919a;
ALTER TABLE accelerator_judgeapplicationfeedback_viewers DROP FOREIGN KEY b92be6a349b66961d369fede7fc32c7f;
ALTER TABLE accelerator_judgeapplicationfeedback_viewers DROP FOREIGN KEY mc_judgeapplicationfeed_user_id_18c5effc7b13a855_fk_auth_user_id;
ALTER TABLE accelerator_judgeavailability DROP FOREIGN KEY commitment_id_refs_id_44f254f6c704321e;
ALTER TABLE accelerator_judgeavailability DROP FOREIGN KEY mc_judgeavailability_panel_location_id_3385fbae70f70c9d_fk;
ALTER TABLE accelerator_judgeavailability DROP FOREIGN KEY mc_judgeavailability_panel_type_id_22a3b26b20eeb6e8_fk;
ALTER TABLE accelerator_judgeavailability DROP FOREIGN KEY panel_time_id_refs_id_1f100ed1682f2ec6;
ALTER TABLE accelerator_judgefeedbackcomponent DROP FOREIGN KEY feedback_element_id_refs_id_54d63a9dd219c340;
ALTER TABLE accelerator_judgefeedbackcomponent DROP FOREIGN KEY judge_feedback_id_refs_id_4b0ec21190418310;
ALTER TABLE accelerator_judgepanelassignment DROP FOREIGN KEY judge_id_refs_id_2e53b26d8b2e6346;
ALTER TABLE accelerator_judgepanelassignment DROP FOREIGN KEY panel_id_refs_id_1a1d9102228bb270;
ALTER TABLE accelerator_judgepanelassignment DROP FOREIGN KEY scenario_id_refs_id_3e0e5c1c02b44c5b;
ALTER TABLE accelerator_judgeroundcommitment DROP FOREIGN KEY judge_id_refs_id_23f940ec2b2eef0;
ALTER TABLE accelerator_judgeroundcommitment DROP FOREIGN KEY judging_round_id_refs_id_2e1cd73270a75621;
ALTER TABLE accelerator_judgingformelement DROP FOREIGN KEY application_question_id_refs_id_1e8585dee6892060;
ALTER TABLE accelerator_judgingformelement DROP FOREIGN KEY form_type_id_refs_id_382ba371eeb4018;
ALTER TABLE accelerator_judginground DROP FOREIGN KEY application_type_id_refs_id_6f47be07ec7b84ec;
ALTER TABLE accelerator_judginground DROP FOREIGN KEY feedback_merge_with_id_refs_id_12c10efcc1a2280b;
ALTER TABLE accelerator_judginground DROP FOREIGN KEY judging_form_id_refs_id_4e632bc157e0b3e0;
ALTER TABLE accelerator_judginground DROP FOREIGN KEY mc__confirmed_judge_label_id_46054c189748a62b_fk_mc_userlabel_id;
ALTER TABLE accelerator_judginground DROP FOREIGN KEY mc_ju_desired_judge_label_id_3abf6794e8853ae4_fk_mc_userlabel_id;
ALTER TABLE accelerator_judginground DROP FOREIGN KEY mc_judgi_startup_label_id_12646c8cbb818997_fk_mc_startuplabel_id;
ALTER TABLE accelerator_judginground DROP FOREIGN KEY program_id_refs_id_4472e0aeb0ea1b8a;
ALTER TABLE accelerator_memberprofile DROP FOREIGN KEY current_program_id_refs_id_272f151a5dd5d322;
ALTER TABLE accelerator_memberprofile DROP FOREIGN KEY user_id_refs_id_66d8d111695cf610;
ALTER TABLE accelerator_memberprofile_interest_categories DROP FOREIGN KEY m_interestcategory_id_7422926df6db4628_fk_mc_interestcategory_id;
ALTER TABLE accelerator_memberprofile_interest_categories DROP FOREIGN KEY mc_memb_memberprofile_id_752cd90e9d0130a2_fk_mc_memberprofile_id;
ALTER TABLE accelerator_memberprofile_program_families DROP FOREIGN KEY mc_memb_programfamily_id_6b0fe4f6a30c3fb6_fk_mc_programfamily_id;
ALTER TABLE accelerator_memberprofile_program_families DROP FOREIGN KEY mc_membe_memberprofile_id_929b254027cc1af_fk_mc_memberprofile_id;
ALTER TABLE accelerator_memberprofile_recommendation_tags DROP FOREIGN KEY ddf332b661ddab44950eb2cd13fd713c;
ALTER TABLE accelerator_memberprofile_recommendation_tags DROP FOREIGN KEY mc_memb_memberprofile_id_19d20fb286cc9a4c_fk_mc_memberprofile_id;
ALTER TABLE accelerator_mentorprogramofficehour DROP FOREIGN KEY finalist_id_refs_id_7a32d211b26580ec;
ALTER TABLE accelerator_mentorprogramofficehour DROP FOREIGN KEY mentor_id_refs_id_7a32d211b26580ec;
ALTER TABLE accelerator_mentorprogramofficehour DROP FOREIGN KEY program_id_refs_id_1209dc2deb18fe46;
ALTER TABLE accelerator_newsletter DROP FOREIGN KEY mc_newsl_judging_round_id_184783f079f722e1_fk_mc_judginground_id;
ALTER TABLE accelerator_newsletter DROP FOREIGN KEY program_id_refs_id_486be2905ede585;
ALTER TABLE accelerator_newsletter_recipient_roles DROP FOREIGN KEY mc_newslett_programrole_id_1d9b5be9d205b028_fk_mc_programrole_id;
ALTER TABLE accelerator_newsletter_recipient_roles DROP FOREIGN KEY mc_newsletter_newsletter_id_202e61d158de2eec_fk_mc_newsletter_id;
ALTER TABLE accelerator_newsletterreceipt DROP FOREIGN KEY newsletter_id_refs_id_69da804eb17d58f6;
ALTER TABLE accelerator_newsletterreceipt DROP FOREIGN KEY recipient_id_refs_id_6b6b3b7bdd7e6690;
ALTER TABLE accelerator_nodepublishedfor DROP FOREIGN KEY node_id_refs_id_7668734e349715a5;
ALTER TABLE accelerator_nodepublishedfor DROP FOREIGN KEY published_for_id_refs_id_4921996d9d58f41;
ALTER TABLE accelerator_observer_newsletter_cc_roles DROP FOREIGN KEY mc_observer__programrole_id_9a41ac9ff4a847a_fk_mc_programrole_id;
ALTER TABLE accelerator_observer_newsletter_cc_roles DROP FOREIGN KEY mc_observer_newsl_observer_id_1cd756e0597ffa2f_fk_mc_observer_id;
ALTER TABLE accelerator_panel DROP FOREIGN KEY mc_panel_location_id_380097c6504c912c_fk;
ALTER TABLE accelerator_panel DROP FOREIGN KEY mc_panel_panel_type_id_766c2e5ff97a78d2_fk;
ALTER TABLE accelerator_panel DROP FOREIGN KEY panel_time_id_refs_id_174f8daa48808dc;
ALTER TABLE accelerator_panellocation DROP FOREIGN KEY judging_round_id_refs_id_35a0f96a66e805d1;
ALTER TABLE accelerator_paneltime DROP FOREIGN KEY judging_round_id_refs_id_fb3f1239d0c7143;
ALTER TABLE accelerator_paneltype DROP FOREIGN KEY judging_round_id_refs_id_51ed88ddea1bd320;
ALTER TABLE accelerator_partner DROP FOREIGN KEY mc_partner_organization_id_98fe7bc40bb29ca_fk_mc_organization_id;
ALTER TABLE accelerator_partnerteammember DROP FOREIGN KEY partner_id_refs_id_3fc4e7d1f80d0752;
ALTER TABLE accelerator_partnerteammember DROP FOREIGN KEY team_member_id_refs_id_6c06035ae98cecae;
ALTER TABLE accelerator_paypalpayment DROP FOREIGN KEY mc_paypalpayment_cycle_id_9338e323147acdb_fk_mc_programcycle_id;
ALTER TABLE accelerator_paypalpayment DROP FOREIGN KEY mc_paypalpayment_startup_id_a452d6a9c7377c6_fk_mc_startup_id;
ALTER TABLE accelerator_paypalrefund DROP FOREIGN KEY mc_paypalrefu_payment_id_14fdef3fc268286c_fk_mc_paypalpayment_id;
ALTER TABLE accelerator_program DROP FOREIGN KEY mc__mentor_program_group_id_290821dbffcfb6ad_fk_mc_namedgroup_id;
ALTER TABLE accelerator_program DROP FOREIGN KEY mc_program_cycle_id_61ff026c4e9874d6_fk_mc_programcycle_id;
ALTER TABLE accelerator_programcycle DROP FOREIGN KEY D2b532926918a76189b007bc07112d14;
ALTER TABLE accelerator_programcycle DROP FOREIGN KEY D8fa969c4dd17aa719c0f7ef8e607772;
ALTER TABLE accelerator_programoverride DROP FOREIGN KEY mc_programoverri_cycle_id_7538130f79fdb192_fk_mc_programcycle_id;
ALTER TABLE accelerator_programoverride DROP FOREIGN KEY program_id_refs_id_7570636eaeb2a465;
ALTER TABLE accelerator_programpartner DROP FOREIGN KEY partner_id_refs_id_32013007824290dc;
ALTER TABLE accelerator_programpartner DROP FOREIGN KEY partner_type_id_refs_id_74ce1d0dcf90fb51;
ALTER TABLE accelerator_programpartner DROP FOREIGN KEY program_id_refs_id_54e90d1cf06e3d56;
ALTER TABLE accelerator_programpartnertype DROP FOREIGN KEY program_id_refs_id_36f206d467928a92;
ALTER TABLE accelerator_programrole DROP FOREIGN KEY mc_programrole_user_label_id_69e5f79c4fc2c69f_fk_mc_userlabel_id;
ALTER TABLE accelerator_programrole DROP FOREIGN KEY program_id_refs_id_5589e8ca800fd225;
ALTER TABLE accelerator_programrole DROP FOREIGN KEY user_role_id_refs_id_33207aed23234109;
ALTER TABLE accelerator_programrolegrant DROP FOREIGN KEY person_id_refs_id_215c7e0829ed91da;
ALTER TABLE accelerator_programrolegrant DROP FOREIGN KEY program_role_id_refs_id_138bb57401e5ad20;
ALTER TABLE accelerator_programstartupattribute DROP FOREIGN KEY program_id_refs_id_6f937825e2472b0;
ALTER TABLE accelerator_programstartupstatus DROP FOREIGN KEY mc_program_startup_role_id_18a0ee32b7188b0b_fk_mc_startuprole_id;
ALTER TABLE accelerator_programstartupstatus DROP FOREIGN KEY program_id_refs_id_5d708c245f24e331;
ALTER TABLE accelerator_reference DROP FOREIGN KEY application_id_refs_id_1cb6cebf80d5703a;
ALTER TABLE accelerator_reference DROP FOREIGN KEY mc_reference_requesting_user_id_5fda2b12709de33e_fk_auth_user_id;
ALTER TABLE accelerator_refundcode DROP FOREIGN KEY mc_refundcode_issued_to_id_5a6a15a5a3522b1_fk_mc_partner_id;
ALTER TABLE accelerator_refundcode_programs DROP FOREIGN KEY mc_refundcode_progr_program_id_476a1ac1e58fc045_fk_mc_program_id;
ALTER TABLE accelerator_refundcode_programs DROP FOREIGN KEY mc_refundcode_refundcode_id_1000b5d2e2207671_fk_mc_refundcode_id;
ALTER TABLE accelerator_refundcoderedemption DROP FOREIGN KEY mc_refundcodered_cycle_id_3fce824be0457a6d_fk_mc_programcycle_id;
ALTER TABLE accelerator_refundcoderedemption DROP FOREIGN KEY mc_refundcoderedemp_startup_id_21b0be308b449a34_fk_mc_startup_id;
ALTER TABLE accelerator_refundcoderedemption DROP FOREIGN KEY refund_code_id_refs_id_1d7938b8e3e5b218;
ALTER TABLE accelerator_scenarioapplication DROP FOREIGN KEY application_id_refs_id_eba383b8b909f05;
ALTER TABLE accelerator_scenarioapplication DROP FOREIGN KEY scenario_id_refs_id_2f17d7079a08ad7a;
ALTER TABLE accelerator_scenariojudge DROP FOREIGN KEY judge_id_refs_id_3d860029a0e7ae4e;
ALTER TABLE accelerator_scenariojudge DROP FOREIGN KEY scenario_id_refs_id_3352d89512fa5faf;
ALTER TABLE accelerator_scenariopreference DROP FOREIGN KEY scenario_id_refs_id_778a93ab767dedb6;
ALTER TABLE accelerator_section DROP FOREIGN KEY newsletter_id_refs_id_5cc0bc71be6b4b70;
ALTER TABLE accelerator_section_interest_categories DROP FOREIGN KEY m_interestcategory_id_180b63e6adfab486_fk_mc_interestcategory_id;
ALTER TABLE accelerator_section_interest_categories DROP FOREIGN KEY mc_section_interest_section_id_6765b81994ce53ca_fk_mc_section_id;
ALTER TABLE accelerator_siteprogramauthorization DROP FOREIGN KEY program_id_refs_id_973861a90a3d578;
ALTER TABLE accelerator_siteprogramauthorization DROP FOREIGN KEY site_id_refs_id_23b3a0e24e71edc2;
ALTER TABLE accelerator_startup DROP FOREIGN KEY user_id_refs_id_6b1225c67f892f18;
ALTER TABLE accelerator_startup_recommendation_tags DROP FOREIGN KEY D7ab1977348253f6d99fd15b574561b2;
ALTER TABLE accelerator_startup_recommendation_tags DROP FOREIGN KEY mc_startup_recommen_startup_id_67290c17cb7f6e48_fk_mc_startup_id;
ALTER TABLE accelerator_startupattribute DROP FOREIGN KEY attribute_id_refs_id_65fe351d295bce44;
ALTER TABLE accelerator_startupattribute DROP FOREIGN KEY startup_id_refs_id_63642cda78edc0e;
ALTER TABLE accelerator_startupcycleinterest DROP FOREIGN KEY mc_startupcyclei_cycle_id_63ec9117ac740358_fk_mc_programcycle_id;
ALTER TABLE accelerator_startupcycleinterest DROP FOREIGN KEY mc_startupcycleinte_startup_id_2b9d8c84ce38794f_fk_mc_startup_id;
ALTER TABLE accelerator_startuplabel_startups DROP FOREIGN KEY mc_startu_startuplabel_id_4ec94364338d2284_fk_mc_startuplabel_id;
ALTER TABLE accelerator_startuplabel_startups DROP FOREIGN KEY mc_startuplabel_sta_startup_id_33e8a0b43d2fac53_fk_mc_startup_id;
ALTER TABLE accelerator_startupmentorrelationship DROP FOREIGN KEY mentor_id_refs_id_69fb20af11568f5f;
ALTER TABLE accelerator_startupmentorrelationship DROP FOREIGN KEY startup_mentor_tracking_id_refs_id_19c20b4e238d9343;
ALTER TABLE accelerator_startupmentortrackingrecord DROP FOREIGN KEY program_id_refs_id_32b32b35fc16168b;
ALTER TABLE accelerator_startupmentortrackingrecord DROP FOREIGN KEY startup_id_refs_id_174176547e67ac4;
ALTER TABLE accelerator_startupoverridegrant DROP FOREIGN KEY program_override_id_refs_id_9ba554d03c6fe87;
ALTER TABLE accelerator_startupoverridegrant DROP FOREIGN KEY startup_id_refs_id_349d7aa842b698c8;
ALTER TABLE accelerator_startupprograminterest DROP FOREIGN KEY c708cc6a4ef0a7fed91a1149d2bcbf3c;
ALTER TABLE accelerator_startupprograminterest DROP FOREIGN KEY mc_startupprogramin_program_id_730ba2c52b7dc808_fk_mc_program_id;
ALTER TABLE accelerator_startupprograminterest DROP FOREIGN KEY mc_startupprogramin_startup_id_2d6e53cf28ee4903_fk_mc_startup_id;
ALTER TABLE accelerator_startupstatus DROP FOREIGN KEY program_startup_status_id_refs_id_164be8ec89b9f8d0;
ALTER TABLE accelerator_startupstatus DROP FOREIGN KEY startup_id_refs_id_112519582f25807d;
ALTER TABLE accelerator_startupteammember DROP FOREIGN KEY startup_id_refs_id_56d2f0da5502cce8;
ALTER TABLE accelerator_startupteammember DROP FOREIGN KEY user_id_refs_id_45c6fbdd2ad623d;
ALTER TABLE accelerator_startupteammember_recommendation_tags DROP FOREIGN KEY D274687269a1a79c1b5809450de49130;
ALTER TABLE accelerator_startupteammember_recommendation_tags DROP FOREIGN KEY d576b6ac2dba85a9496621cfa7a87d28;
ALTER TABLE accelerator_userlabel_users DROP FOREIGN KEY mc_userlabel_us_userlabel_id_50cdfbb02f325003_fk_mc_userlabel_id;
ALTER TABLE accelerator_userlabel_users DROP FOREIGN KEY mc_userlabel_users_user_id_6933accf268979f0_fk_auth_user_id;

ALTER TABLE accelerator_startup_related_industry DROP FOREIGN KEY mc_startup_related__startup_id_6e5e21607c907ea2_fk_mc_startup_id;
ALTER TABLE accelerator_startup_related_industry DROP FOREIGN KEY mc_startup_relate_industry_id_1e341ac512b458e8_fk_mc_industry_id;
ALTER TABLE accelerator_startup DROP FOREIGN KEY mc_startu_currency_id_a24d833928e93ed_fk_accelerator_currency_id;
ALTER TABLE accelerator_startup DROP FOREIGN KEY mc_startu_primary_industry_id_3ef9d143bc4885a7_fk_mc_industry_id;
ALTER TABLE accelerator_startup DROP FOREIGN KEY mc_startup_organization_id_f0c141ee70010ad_fk_mc_organization_id;

ALTER TABLE accelerator_scenario DROP FOREIGN KEY mc_scena_judging_round_id_1d1fc99a8e6d1854_fk_mc_judginground_id;
ALTER TABLE accelerator_program DROP FOREIGN KEY mc_pro_program_family_id_16b19eeca84d9464_fk_mc_programfamily_id;
ALTER TABLE accelerator_expertprofile DROP FOREIGN KEY mc_expert_primary_industry_id_40f595482b3c599b_fk_mc_industry_id;
ALTER TABLE accelerator_expert_related_industry DROP FOREIGN KEY mc_expe_expertprofile_id_77c2d7a8d016a072_fk_mc_expertprofile_id;
ALTER TABLE accelerator_expert_related_industry DROP FOREIGN KEY mc_expert_related_industry_id_3eb7742751e1c56a_fk_mc_industry_id;

-- still not working (missing)
-- ALTER TABLE accelerator_refundcoderedemption DROP FOREIGN KEY mc_refundco_redeemed_by_id_3739dad9f8401416_fk_mc_application_id;
-- ALTER TABLE pagetype_accelerator_categoryheaderpage DROP FOREIGN KEY urlnode_ptr_id_refs_id_3840110913794bb5;
-- ALTER TABLE pagetype_accelerator_filepage DROP FOREIGN KEY urlnode_ptr_id_refs_id_377f6c6f6024dc4c;

ALTER TABLE pagetype_accelerator_siteredirectpage DROP FOREIGN KEY urlnode_ptr_id_refs_id_468c11ed732a5359;
ALTER TABLE pagetype_accelerator_userrolemenu DROP FOREIGN KEY paget_urlnode_ptr_id_2f39dc373fe22072_fk_fluent_pages_urlnode_id;
ALTER TABLE pagetype_accelerator_userrolemenu DROP FOREIGN KEY pagetyp_program_family_id_c6e7ccad603a44c_fk_mc_programfamily_id;
ALTER TABLE pagetype_accelerator_userrolemenu DROP FOREIGN KEY pagetype_mc_user_user_role_id_6cac5fbcc4d13adc_fk_mc_userrole_id;
ALTER TABLE pagetype_accelerator_userrolemenu DROP FOREIGN KEY pagetype_mc_userrol_program_id_7eeaf62a8a1e191a_fk_mc_program_id;

-- Drop unique index


ALTER TABLE accelerator_clearance DROP INDEX mc_clearance_user_id_764602837aad43f1_uniq;
ALTER TABLE accelerator_entrepreneurprofile_interest_categories DROP INDEX mc_entrepreneurpro_entrepreneurprofile_id_4523906403fd95f0_uniq;
ALTER TABLE accelerator_entrepreneurprofile_program_families DROP INDEX mc_entrepreneurpro_entrepreneurprofile_id_45dde2434621f03a_uniq;
ALTER TABLE accelerator_entrepreneurprofile_recommendation_tags DROP INDEX mc_entrepreneurpro_entrepreneurprofile_id_322df36b16f6ec54_uniq;
ALTER TABLE accelerator_expert_related_industry DROP INDEX mc_expert_related_indust_expertprofile_id_19181e4364289430_uniq;
ALTER TABLE accelerator_expert_related_mentoringspecialty DROP INDEX mc_expert_related_mentor_expertprofile_id_53f3c886bc5e586e_uniq;
ALTER TABLE accelerator_expertprofile_functional_expertise DROP INDEX mc_expertprofile_function_expertprofile_id_6c541566600e150_uniq;
ALTER TABLE accelerator_expertprofile_interest_categories DROP INDEX mc_expertprofile_interes_expertprofile_id_764150abf55a75c0_uniq;
ALTER TABLE accelerator_expertprofile_program_families DROP INDEX mc_expertprofile_program_expertprofile_id_6f3222a509a35d42_uniq;
ALTER TABLE accelerator_expertprofile_recommendation_tags DROP INDEX mc_expertprofile_recomme_expertprofile_id_3df8d461fa233b3a_uniq;
ALTER TABLE accelerator_judgeapplicationfeedback DROP INDEX mc_judgeapplicationfeedback_judge_id_70ef10bbe77ffc82_uniq;
ALTER TABLE accelerator_judgeavailability DROP INDEX mc_judgeavailability_commitment_id_38b962faff131c43_uniq;
ALTER TABLE accelerator_judgefeedbackcomponent DROP INDEX mc_judgefeedbackcompo_feedback_element_id_4d3bc9f4668678fe_uniq;
ALTER TABLE accelerator_judgepanelassignment DROP INDEX mc_judgepanelassignment_judge_id_30b854c0fc612ceb_uniq;
ALTER TABLE accelerator_judgeroundcommitment DROP INDEX mc_judgeroundcommitment_judge_id_3d1fe8bc1847797a_uniq;
ALTER TABLE accelerator_judginground DROP INDEX mc_judginground_program_id_670d689f64eaff1d_uniq;
ALTER TABLE accelerator_memberprofile_interest_categories DROP INDEX mc_memberprofile_interes_memberprofile_id_42ef6b43fb37b0dc_uniq;
ALTER TABLE accelerator_memberprofile_program_families DROP INDEX mc_memberprofile_program_memberprofile_id_2520e8078b5f622e_uniq;
ALTER TABLE accelerator_memberprofile_recommendation_tags DROP INDEX mc_memberprofile_recomme_memberprofile_id_4007ecf009453f3a_uniq;
ALTER TABLE accelerator_mentorprogramofficehour DROP INDEX mc_mentorprogramofficehour_program_id_67770dd7afd85768_uniq;
ALTER TABLE accelerator_newsletter_recipient_roles DROP INDEX mc_newsletter_recipient_rol_newsletter_id_749b2e4648db18d9_uniq;

ALTER TABLE accelerator_partnerteammember DROP INDEX mc_partnerteammember_partner_id_63570f79ede4df50_uniq;
ALTER TABLE accelerator_programrolegrant DROP INDEX mc_programrolegrant_person_id_6ec78927b617036e_uniq;
ALTER TABLE accelerator_programstartupattribute DROP INDEX mc_programstartupattribute_program_id_112d0591fc7af0a_uniq;
ALTER TABLE accelerator_refundcode_programs DROP INDEX mc_refundcode_programs_refundcode_id_3f17a00435ed3b94_uniq;
ALTER TABLE accelerator_scenarioapplication DROP INDEX mc_scenarioapplication_scenario_id_163e3335590fe4d2_uniq;
ALTER TABLE accelerator_scenariojudge DROP INDEX mc_scenariojudge_scenario_id_67fa0bcd38d447be_uniq;
ALTER TABLE accelerator_scenariopreference DROP INDEX mc_scenariopreference_scenario_id_2e5f7d3baec37a3e_uniq;
ALTER TABLE accelerator_section_interest_categories DROP INDEX mc_section_interest_categories_section_id_7ae83d6e54a7dfb0_uniq;
ALTER TABLE accelerator_siteprogramauthorization DROP INDEX mc_siteprogramauthorization_site_id_6d23da31460b4b00_uniq;
ALTER TABLE accelerator_startup_recommendation_tags DROP INDEX mc_startup_recommendation_tags_startup_id_7c5983575634af26_uniq;
ALTER TABLE accelerator_startup_related_industry DROP INDEX mc_startup_related_industry_startup_id_30c98f9faa444c3c_uniq;
ALTER TABLE accelerator_startupmentortrackingrecord DROP INDEX mc_startupmentortrackingrecord_startup_id_10b8df6326e8e6ae_uniq;
ALTER TABLE accelerator_startupstatus DROP INDEX mc_startupstatus_startup_id_12a679a3af235aad_uniq;
ALTER TABLE accelerator_startupteammember DROP INDEX mc_startupteammember_startup_id_238984adddc26700_uniq;
ALTER TABLE accelerator_startupteammember_recommendation_tags DROP INDEX mc_startupteammember_startupteammember_id_4654591bbb270440_uniq;

ALTER TABLE accelerator_application DROP INDEX mc_application_d7b272e0;
ALTER TABLE accelerator_application DROP INDEX mc_application_ca71274b;
ALTER TABLE accelerator_application DROP INDEX mc_application_92fe01c8;
ALTER TABLE accelerator_applicationanswer DROP INDEX mc_applicationanswer_398529ef;
ALTER TABLE accelerator_applicationanswer DROP INDEX mc_applicationanswer_14a50a7d;
ALTER TABLE accelerator_applicationpanelassignment DROP INDEX mc_applicationpanelassignment_398529ef;
ALTER TABLE accelerator_applicationpanelassignment DROP INDEX mc_applicationpanelassignment_130efbb7;
ALTER TABLE accelerator_applicationpanelassignment DROP INDEX mc_applicationpanelassignment_3bb529ba;
ALTER TABLE accelerator_applicationquestion DROP INDEX mc_applicationquestion_ca71274b;
ALTER TABLE accelerator_applicationquestion DROP INDEX mc_applicationquestion_7aa0f6ee;
ALTER TABLE accelerator_applicationquestion DROP INDEX mc_applicationquestion_429b1823;
ALTER TABLE accelerator_applicationtype DROP INDEX mc_applicationtype_fcd6cf16;
ALTER TABLE accelerator_bucketstate DROP INDEX mc_bucketstate_cycle_id_48a9f2e6a10a0b57_fk_mc_programcycle_id;
ALTER TABLE accelerator_bucketstate DROP INDEX mc_buckets_program_role_id_4d187fafc6f72c1b_fk_mc_programrole_id;
ALTER TABLE accelerator_clearance DROP INDEX mc_cle_program_family_id_1121ea2a0e27cb3c_fk_mc_programfamily_id;
ALTER TABLE accelerator_entrepreneurprofile DROP INDEX mc_entrepreneurprofile_3ff4c9e5;
ALTER TABLE accelerator_entrepreneurprofile_interest_categories DROP INDEX mc_entrepreneurprofile_interest_categories_35e701e5;
ALTER TABLE accelerator_entrepreneurprofile_interest_categories DROP INDEX mc_entrepreneurprofile_interest_categories_3ba61f0a;
ALTER TABLE accelerator_entrepreneurprofile_program_families DROP INDEX mc_entrepreneurprofile_program_families_35e701e5;
ALTER TABLE accelerator_entrepreneurprofile_program_families DROP INDEX mc_entrepreneurprofile_program_families_d2344029;
ALTER TABLE accelerator_entrepreneurprofile_recommendation_tags DROP INDEX mc_entrepreneurprofile_recommendation_tags_35e701e5;
ALTER TABLE accelerator_entrepreneurprofile_recommendation_tags DROP INDEX mc_entrepreneurprofile_recommendation_tags_d1dd995a;
ALTER TABLE accelerator_expert_related_industry DROP INDEX mc_expert_related_industry_ab5ddbd6;
ALTER TABLE accelerator_expert_related_industry DROP INDEX mc_expert_related_industry_d28c39ae;
ALTER TABLE accelerator_expert_related_mentoringspecialty DROP INDEX mc_expert_related_mentoringspecialty_ab5ddbd6;
ALTER TABLE accelerator_expert_related_mentoringspecialty DROP INDEX mc_expert_related_mentoringspecialty_c8f3748f;
ALTER TABLE accelerator_expertinterest DROP INDEX mc_expertinterest_fbfc09f1;
ALTER TABLE accelerator_expertinterest DROP INDEX mc_expertinterest_8d00c2c3;
ALTER TABLE accelerator_expertinterest DROP INDEX mc_expertinterest_4322a5c8;
ALTER TABLE accelerator_expertprofile DROP INDEX mc_expertprofile_13b5d1c8;
ALTER TABLE accelerator_expertprofile DROP INDEX mc_expertprofile_1d397c99;
ALTER TABLE accelerator_expertprofile DROP INDEX mc_expertprofile_3ff4c9e5;
ALTER TABLE accelerator_expertprofile DROP INDEX mc_expertprofile_9459abc0;
ALTER TABLE accelerator_expertprofile_functional_expertise DROP INDEX mc_expertprofile_functional_expertise_ab5ddbd6;
ALTER TABLE accelerator_expertprofile_functional_expertise DROP INDEX mc_expertprofile_functional_expertise_661e48e7;
ALTER TABLE accelerator_expertprofile_interest_categories DROP INDEX mc_expertprofile_interest_categories_ab5ddbd6;
ALTER TABLE accelerator_expertprofile_interest_categories DROP INDEX mc_expertprofile_interest_categories_3ba61f0a;
ALTER TABLE accelerator_expertprofile_program_families DROP INDEX mc_expertprofile_program_families_ab5ddbd6;
ALTER TABLE accelerator_expertprofile_program_families DROP INDEX mc_expertprofile_program_families_d2344029;
ALTER TABLE accelerator_expertprofile_recommendation_tags DROP INDEX mc_expertprofile_recommendation_tags_ab5ddbd6;
ALTER TABLE accelerator_expertprofile_recommendation_tags DROP INDEX mc_expertprofile_recommendation_tags_d1dd995a;
ALTER TABLE accelerator_functionalexpertise DROP INDEX mc_functionalexpertise_63f17a16;
ALTER TABLE accelerator_functionalexpertise DROP INDEX mc_functionalexpertise_42b06ff6;
ALTER TABLE accelerator_functionalexpertise DROP INDEX mc_functionalexpertise_91543e5a;
ALTER TABLE accelerator_functionalexpertise DROP INDEX mc_functionalexpertise_efd07f28;
ALTER TABLE accelerator_functionalexpertise DROP INDEX mc_functionalexpertise_2a8f42e8;
ALTER TABLE accelerator_industry DROP INDEX mc_industry_63f17a16;
ALTER TABLE accelerator_industry DROP INDEX mc_industry_42b06ff6;
ALTER TABLE accelerator_industry DROP INDEX mc_industry_91543e5a;
ALTER TABLE accelerator_industry DROP INDEX mc_industry_efd07f28;
ALTER TABLE accelerator_industry DROP INDEX mc_industry_2a8f42e8;
ALTER TABLE accelerator_interestcategory DROP INDEX mc_interestcategory_7eef53e3;
ALTER TABLE accelerator_jobposting DROP INDEX mc_jobposting_92fe01c8;
ALTER TABLE accelerator_judgeapplicationfeedback DROP INDEX mc_judgeapplicationfeedback_398529ef;
ALTER TABLE accelerator_judgeapplicationfeedback DROP INDEX mc_judgeapplicationfeedback_a2e1b040;
ALTER TABLE accelerator_judgeapplicationfeedback DROP INDEX mc_judgeapplicationfeedback_bcb024b0;
ALTER TABLE accelerator_judgeapplicationfeedback DROP INDEX mc_judgeapplicationfeedback_130efbb7;
ALTER TABLE accelerator_judgeapplicationfeedback_viewers DROP INDEX mc_judgeapplicationfeed_user_id_18c5effc7b13a855_fk_auth_user_id;
ALTER TABLE accelerator_judgeavailability DROP INDEX mc_judgeavailability_6a6b8869;
ALTER TABLE accelerator_judgeavailability DROP INDEX mc_judgeavailability_abc2343a;
ALTER TABLE accelerator_judgeavailability DROP INDEX mc_judgeavailability_efe7ff4c;
ALTER TABLE accelerator_judgeavailability DROP INDEX mc_judgeavailability_44f22665;
ALTER TABLE accelerator_judgefeedbackcomponent DROP INDEX mc_judgefeedbackcomponent_206f544c;
ALTER TABLE accelerator_judgefeedbackcomponent DROP INDEX mc_judgefeedbackcomponent_5691d10d;
ALTER TABLE accelerator_judgefeedbackcomponent DROP INDEX mc_judgefeedbackcomponent_id_4ab8b943d37a3a60_idx;
ALTER TABLE accelerator_judgepanelassignment DROP INDEX mc_judgepanelassignment_bcb024b0;
ALTER TABLE accelerator_judgepanelassignment DROP INDEX mc_judgepanelassignment_130efbb7;
ALTER TABLE accelerator_judgepanelassignment DROP INDEX mc_judgepanelassignment_3bb529ba;
ALTER TABLE accelerator_judgeroundcommitment DROP INDEX mc_judgeroundcommitment_bcb024b0;
ALTER TABLE accelerator_judgeroundcommitment DROP INDEX mc_judgeroundcommitment_7164203c;
ALTER TABLE accelerator_judgingformelement DROP INDEX mc_judgingformelement_a2e1b040;
ALTER TABLE accelerator_judgingformelement DROP INDEX mc_judgingformelement_14a50a7d;
ALTER TABLE accelerator_judginground DROP INDEX mc_judginground_7eef53e3;
ALTER TABLE accelerator_judginground DROP INDEX mc_judginground_ca71274b;
ALTER TABLE accelerator_judginground DROP INDEX mc_judginground_beebb9e3;
ALTER TABLE accelerator_judginground DROP INDEX mc_judginground_be093638;
ALTER TABLE accelerator_judginground DROP INDEX mc_judginground_413c41b4;
ALTER TABLE accelerator_judginground DROP INDEX mc_judginground_5926436d;
ALTER TABLE accelerator_judginground DROP INDEX mc_judginground_bdf8c73e;
ALTER TABLE accelerator_memberprofile DROP INDEX mc_memberprofile_3ff4c9e5;
ALTER TABLE accelerator_memberprofile_interest_categories DROP INDEX mc_memberprofile_interest_categories_9b34fcb0;
ALTER TABLE accelerator_memberprofile_interest_categories DROP INDEX mc_memberprofile_interest_categories_3ba61f0a;
ALTER TABLE accelerator_memberprofile_program_families DROP INDEX mc_memberprofile_program_families_9b34fcb0;
ALTER TABLE accelerator_memberprofile_program_families DROP INDEX mc_memberprofile_program_families_d2344029;
ALTER TABLE accelerator_memberprofile_recommendation_tags DROP INDEX mc_memberprofile_recommendation_tags_9b34fcb0;
ALTER TABLE accelerator_memberprofile_recommendation_tags DROP INDEX mc_memberprofile_recommendation_tags_d1dd995a;
ALTER TABLE accelerator_mentorprogramofficehour DROP INDEX mc_mentorprogramofficehour_7eef53e3;
ALTER TABLE accelerator_mentorprogramofficehour DROP INDEX mc_mentorprogramofficehour_cea652a7;
ALTER TABLE accelerator_mentorprogramofficehour DROP INDEX mc_mentorprogramofficehour_6f9cffd0;
ALTER TABLE accelerator_mentorprogramofficehour DROP INDEX mc_mentorprogramofficehour_effd9ef;
ALTER TABLE accelerator_mentorprogramofficehour DROP INDEX mc_mentorprogramofficehour_986cbc25;
ALTER TABLE accelerator_mentorprogramofficehour DROP INDEX mc_mentorprogramofficehour_801e862;
ALTER TABLE accelerator_newsletter DROP INDEX mc_newsletter_7eef53e3;
ALTER TABLE accelerator_newsletter DROP INDEX mc_newsletter_0cc25dbd;
ALTER TABLE accelerator_newsletter_recipient_roles DROP INDEX mc_newsletter_recipient_roles_50580fc3;
ALTER TABLE accelerator_newsletter_recipient_roles DROP INDEX mc_newsletter_recipient_roles_f3d1817;
ALTER TABLE accelerator_newsletterreceipt DROP INDEX mc_newlettersenttorecipient_50580fc3;
ALTER TABLE accelerator_newsletterreceipt DROP INDEX mc_newlettersenttorecipient_fcd09624;
ALTER TABLE accelerator_nodepublishedfor DROP INDEX mc_nodepublishedfor_474baebc;
ALTER TABLE accelerator_nodepublishedfor DROP INDEX mc_nodepublishedfor_300b475b;
ALTER TABLE accelerator_observer_newsletter_cc_roles DROP INDEX mc_observer__programrole_id_9a41ac9ff4a847a_fk_mc_programrole_id;
ALTER TABLE accelerator_panel DROP INDEX mc_panel_efe7ff4c;
ALTER TABLE accelerator_panel DROP INDEX mc_panel_44f22665;
ALTER TABLE accelerator_panel DROP INDEX mc_panel_319d859;
ALTER TABLE accelerator_panellocation DROP INDEX mc_panellocation_7164203c;
ALTER TABLE accelerator_paneltime DROP INDEX mc_paneltime_7164203c;
ALTER TABLE accelerator_paneltype DROP INDEX mc_paneltype_7164203c;
ALTER TABLE accelerator_partner DROP INDEX mc_partner_26b2345e;
ALTER TABLE accelerator_partnerteammember DROP INDEX mc_partnerteammember_76043359;
ALTER TABLE accelerator_partnerteammember DROP INDEX mc_partnerteammember_fb893391;
ALTER TABLE accelerator_paypalpayment DROP INDEX mc_paypalpayment_startup_id_a452d6a9c7377c6_fk_mc_startup_id;
ALTER TABLE accelerator_paypalpayment DROP INDEX mc_paypalpayment_d7b272e0;
ALTER TABLE accelerator_paypalrefund DROP INDEX mc_paypalrefund_376ebbba;
ALTER TABLE accelerator_program DROP INDEX mc_program_8d00c2c3;
ALTER TABLE accelerator_program DROP INDEX mc_program_d7b272e0;
ALTER TABLE accelerator_program DROP INDEX mc_program_6c161578;
ALTER TABLE accelerator_programcycle DROP INDEX D2b532926918a76189b007bc07112d14;
ALTER TABLE accelerator_programcycle DROP INDEX D8fa969c4dd17aa719c0f7ef8e607772;
ALTER TABLE accelerator_programoverride DROP INDEX mc_programoverride_7eef53e3;
ALTER TABLE accelerator_programoverride DROP INDEX mc_programoverride_d7b272e0;
ALTER TABLE accelerator_programpartner DROP INDEX mc_programpartner_7eef53e3;
ALTER TABLE accelerator_programpartner DROP INDEX mc_programpartner_76043359;
ALTER TABLE accelerator_programpartner DROP INDEX mc_programpartner_89cc1785;
ALTER TABLE accelerator_programpartnertype DROP INDEX mc_programpartnertype_7eef53e3;
ALTER TABLE accelerator_programrole DROP INDEX mc_programrole_7eef53e3;
ALTER TABLE accelerator_programrole DROP INDEX mc_programrole_52094d6e;
ALTER TABLE accelerator_programrole DROP INDEX mc_programrole_d4ca635b;
ALTER TABLE accelerator_programrole DROP INDEX mc_programrole_75df8002;
ALTER TABLE accelerator_programrolegrant DROP INDEX mc_programrolegrant_21b911c5;
ALTER TABLE accelerator_programrolegrant DROP INDEX mc_programrolegrant_2f8d8f1d;
ALTER TABLE accelerator_programstartupattribute DROP INDEX mc_programstartupattribute_7eef53e3;
ALTER TABLE accelerator_programstartupstatus DROP INDEX mc_programstartupstatus_7eef53e3;
ALTER TABLE accelerator_programstartupstatus DROP INDEX mc_programstartupstatus_5f4af245;
ALTER TABLE accelerator_reference DROP INDEX mc_reference_398529ef;
ALTER TABLE accelerator_reference DROP INDEX mc_reference_f15d121c;
ALTER TABLE accelerator_refundcode DROP INDEX mc_refundcode_1b81f678;
ALTER TABLE accelerator_refundcode_programs DROP INDEX mc_refundcode_programs_88b5e867;
ALTER TABLE accelerator_refundcode_programs DROP INDEX mc_refundcode_programs_7eef53e3;
ALTER TABLE accelerator_refundcoderedemption DROP INDEX mc_refundcoderedemption_79446569;
ALTER TABLE accelerator_refundcoderedemption DROP INDEX mc_refundcoderedemption_99f77c8c;
ALTER TABLE accelerator_refundcoderedemption DROP INDEX mc_refundcoderedemption_d7b272e0;
ALTER TABLE accelerator_scenario DROP INDEX mc_scenario_0cc25dbd;
ALTER TABLE accelerator_scenarioapplication DROP INDEX mc_scenarioapplication_398529ef;
ALTER TABLE accelerator_scenarioapplication DROP INDEX mc_scenarioapplication_3bb529ba;
ALTER TABLE accelerator_scenariojudge DROP INDEX mc_scenariojudge_bcb024b0;
ALTER TABLE accelerator_scenariojudge DROP INDEX mc_scenariojudge_3bb529ba;
ALTER TABLE accelerator_scenariopreference DROP INDEX mc_scenariopreference_3bb529ba;
ALTER TABLE accelerator_section DROP INDEX mc_section_50580fc3;
ALTER TABLE accelerator_section_interest_categories DROP INDEX mc_section_interest_categories_c007bd5a;
ALTER TABLE accelerator_section_interest_categories DROP INDEX mc_section_interest_categories_3ba61f0a;
ALTER TABLE accelerator_siteprogramauthorization DROP INDEX mc_siteprogramauthorization_6223029;
ALTER TABLE accelerator_siteprogramauthorization DROP INDEX mc_siteprogramauthorization_7eef53e3;
ALTER TABLE accelerator_startup DROP INDEX mc_startup_a7244bad;
ALTER TABLE accelerator_startup DROP INDEX user_id_refs_id_6b1225c67f892f18;
ALTER TABLE accelerator_startup DROP INDEX mc_startup_26b2345e;
ALTER TABLE accelerator_startup DROP INDEX mc_startup_7118241e;
ALTER TABLE accelerator_startup_recommendation_tags DROP INDEX mc_startup_recommendation_tags_92fe01c8;
ALTER TABLE accelerator_startup_recommendation_tags DROP INDEX mc_startup_recommendation_tags_d1dd995a;
ALTER TABLE accelerator_startup_related_industry DROP INDEX mc_startup_related_industry_92fe01c8;
ALTER TABLE accelerator_startup_related_industry DROP INDEX mc_startup_related_industry_d28c39ae;
ALTER TABLE accelerator_startupattribute DROP INDEX mc_startupattribute_92fe01c8;
ALTER TABLE accelerator_startupattribute DROP INDEX mc_startupattribute_f2eca69f;
ALTER TABLE accelerator_startupcycleinterest DROP INDEX mc_startupcyclei_cycle_id_63ec9117ac740358_fk_mc_programcycle_id;
ALTER TABLE accelerator_startupcycleinterest DROP INDEX mc_startupcycleinte_startup_id_2b9d8c84ce38794f_fk_mc_startup_id;
ALTER TABLE accelerator_startuplabel_startups DROP INDEX mc_startuplabel_sta_startup_id_33e8a0b43d2fac53_fk_mc_startup_id;
ALTER TABLE accelerator_startupmentorrelationship DROP INDEX mc_startupmentorrelationship_e3c64f20;
ALTER TABLE accelerator_startupmentorrelationship DROP INDEX mc_startupmentorrelationship_cea652a7;
ALTER TABLE accelerator_startupmentortrackingrecord DROP INDEX mc_startupmentortrackingrecord_92fe01c8;
ALTER TABLE accelerator_startupmentortrackingrecord DROP INDEX mc_startupmentortrackingrecord_7eef53e3;
ALTER TABLE accelerator_startupoverridegrant DROP INDEX mc_startupoverridegrant_92fe01c8;
ALTER TABLE accelerator_startupoverridegrant DROP INDEX mc_startupoverridegrant_77a6cd5;
ALTER TABLE accelerator_startupprograminterest DROP INDEX mc_startupprogramin_program_id_730ba2c52b7dc808_fk_mc_program_id;
ALTER TABLE accelerator_startupprograminterest DROP INDEX mc_startupprogramin_startup_id_2d6e53cf28ee4903_fk_mc_startup_id;
ALTER TABLE accelerator_startupprograminterest DROP INDEX mc_startupprograminterest_70a17ffa;
ALTER TABLE accelerator_startupprograminterest DROP INDEX mc_startupprograminterest_f699e0e2;
ALTER TABLE accelerator_startupstatus DROP INDEX mc_startupstatus_92fe01c8;
ALTER TABLE accelerator_startupstatus DROP INDEX mc_startupstatus_4c64f505;
ALTER TABLE accelerator_startupteammember DROP INDEX mc_startupteammember_92fe01c8;
ALTER TABLE accelerator_startupteammember DROP INDEX mc_startupteammember_fbfc09f1;
ALTER TABLE accelerator_startupteammember_recommendation_tags DROP INDEX mc_startupteammember_recommendation_tags_7486611;
ALTER TABLE accelerator_startupteammember_recommendation_tags DROP INDEX mc_startupteammember_recommendation_tags_d1dd995a;
ALTER TABLE accelerator_userlabel_users DROP INDEX mc_userlabel_users_user_id_6933accf268979f0_fk_auth_user_id;
ALTER TABLE accelerator_applicationpanelassignment DROP INDEX mc_applicationpanelassignm_application_id_77696d5c58b0d103_uniq;

ALTER TABLE pagetype_accelerator_userrolemenu DROP INDEX pagetyp_program_family_id_c6e7ccad603a44c_fk_mc_programfamily_id;
ALTER TABLE pagetype_accelerator_userrolemenu DROP INDEX pagetype_mc_user_user_role_id_6cac5fbcc4d13adc_fk_mc_userrole_id;
ALTER TABLE pagetype_accelerator_userrolemenu DROP INDEX pagetype_mc_userrolemenu_429b1823;
ALTER TABLE accelerator_startupteammember_recommendation_tags DROP INDEX mc_startupteammember_recommendation_tags_7486611;



-- did not exist
-- ALTER TABLE accelerator_startup DROP INDEX mc_startup_url_slug_4307d276937cb2aa_uniq;
-- ALTER TABLE accelerator_scenario DROP INDEX mc_scenario_name_47e6539550bf6955_uniq;
-- ALTER TABLE accelerator_scenario DROP INDEX mc_scenario_sequence_number_a97fc5cc088e606_uniq;
-- ALTER TABLE accelerator_partner DROP INDEX mc_partner_name_5f11b39aecd9374b_uniq;
-- ALTER TABLE accelerator_partner DROP INDEX mc_partner_url_slug_2c7587e0d9e00373_uniq;


-- re-add constraints:
--
-- Alter unique_together for startupteammember (1 constraint(s))
--
ALTER TABLE `accelerator_startupteammember` ADD CONSTRAINT `accelerator_startupteammember_startup_id_582d4474_uniq` UNIQUE (`startup_id`, `user_id`);
--
-- Alter unique_together for startupstatus (1 constraint(s))
--
ALTER TABLE `accelerator_startupstatus` ADD CONSTRAINT `accelerator_startupstatus_startup_id_124d9916_uniq` UNIQUE (`startup_id`, `program_startup_status_id`);
--
-- Alter unique_together for startupmentortrackingrecord (1 constraint(s))
--
ALTER TABLE `accelerator_startupmentortrackingrecord` ADD CONSTRAINT `accelerator_startupmentortrackingrecord_startup_id_1242e204_uniq` UNIQUE (`startup_id`, `program_id`);
--
-- Alter unique_together for siteprogramauthorization (1 constraint(s))
--
ALTER TABLE `accelerator_siteprogramauthorization` ADD CONSTRAINT `accelerator_siteprogramauthorization_site_id_aed5187c_uniq` UNIQUE (`site_id`, `program_id`);
--
-- Alter unique_together for scenariopreference (1 constraint(s))
--
ALTER TABLE `accelerator_scenariopreference` ADD CONSTRAINT `accelerator_scenariopreference_scenario_id_5f376349_uniq` UNIQUE (`scenario_id`, `priority`, `entity_type`);
--
-- Alter unique_together for scenariojudge (1 constraint(s))
--
ALTER TABLE `accelerator_scenariojudge` ADD CONSTRAINT `accelerator_scenariojudge_scenario_id_5e6dced4_uniq` UNIQUE (`scenario_id`, `judge_id`);
--
-- Alter unique_together for scenarioapplication (1 constraint(s))
--
ALTER TABLE `accelerator_scenarioapplication` ADD CONSTRAINT `accelerator_scenarioapplication_scenario_id_ff7143f3_uniq` UNIQUE (`scenario_id`, `application_id`);
--
-- Alter unique_together for programstartupattribute (1 constraint(s))
--
ALTER TABLE `accelerator_programstartupattribute` ADD CONSTRAINT `accelerator_programstartupattribute_program_id_1af62fa8_uniq` UNIQUE (`program_id`, `attribute_label`);
--
-- Alter unique_together for programrolegrant (1 constraint(s))
--
ALTER TABLE `accelerator_programrolegrant` ADD CONSTRAINT `accelerator_programrolegrant_person_id_11dc9f10_uniq` UNIQUE (`person_id`, `program_role_id`);
--
-- Alter unique_together for partnerteammember (1 constraint(s))
--
ALTER TABLE `accelerator_partnerteammember` ADD CONSTRAINT `accelerator_partnerteammember_partner_id_bd54ec64_uniq` UNIQUE (`partner_id`, `team_member_id`);
--
-- Alter unique_together for mentorprogramofficehour (1 constraint(s))
--
ALTER TABLE `accelerator_mentorprogramofficehour` ADD CONSTRAINT `accelerator_mentorprogramofficehour_program_id_2905068d_uniq` UNIQUE (`program_id`, `mentor_id`, `date`, `start_time`);
--
-- Alter unique_together for judginground (1 constraint(s))
--
ALTER TABLE `accelerator_judginground` ADD CONSTRAINT `accelerator_judginground_program_id_d179d450_uniq` UNIQUE (`program_id`, `name`);
--
-- Alter unique_together for judgeroundcommitment (1 constraint(s))
--
ALTER TABLE `accelerator_judgeroundcommitment` ADD CONSTRAINT `accelerator_judgeroundcommitment_judge_id_aa4b584b_uniq` UNIQUE (`judge_id`, `judging_round_id`);
--
-- Alter unique_together for judgepanelassignment (1 constraint(s))
--
ALTER TABLE `accelerator_judgepanelassignment` ADD CONSTRAINT `accelerator_judgepanelassignment_judge_id_050c6a17_uniq` UNIQUE (`judge_id`, `panel_id`, `scenario_id`);
--
-- Alter unique_together for judgefeedbackcomponent (1 constraint(s))
--
ALTER TABLE `accelerator_judgefeedbackcomponent` ADD CONSTRAINT `accelerator_judgefeedbackcompone_judge_feedback_id_4acbbfef_uniq` UNIQUE (`judge_feedback_id`, `feedback_element_id`);
--
-- Alter unique_together for judgeavailability (1 constraint(s))
--
ALTER TABLE `accelerator_judgeavailability` ADD CONSTRAINT `accelerator_judgeavailability_commitment_id_0e462608_uniq` UNIQUE (`commitment_id`, `panel_location_id`, `panel_time_id`, `panel_type_id`);
--
-- Alter unique_together for judgeapplicationfeedback (1 constraint(s))
--
ALTER TABLE `accelerator_judgeapplicationfeedback` ADD CONSTRAINT `accelerator_judgeapplicationfeedbac_application_id_949b3b4f_uniq` UNIQUE (`application_id`, `judge_id`, `panel_id`);
--
-- Alter unique_together for clearance (1 constraint(s))
--
ALTER TABLE `accelerator_clearance` ADD CONSTRAINT `accelerator_clearance_user_id_7b9139c2_uniq` UNIQUE (`user_id`, `program_family_id`);
--
-- Alter unique_together for applicationpanelassignment (1 constraint(s))
--
ALTER TABLE `accelerator_applicationpanelassignment` ADD CONSTRAINT `accelerator_applicationpanelassignm_application_id_8506589b_uniq` UNIQUE (`application_id`, `panel_id`, `scenario_id`);
--
-- Alter index_together for judgefeedbackcomponent (1 constraint(s))
--
CREATE INDEX `accelerator_judgefeedbackcomponent_id_2f5f2fba_idx` ON `accelerator_judgefeedbackcomponent` (`id`, `judge_feedback_id`, `feedback_element_id`, `answer_text`);
ALTER TABLE `accelerator_industry` ADD CONSTRAINT `accelerator_indust_parent_id_a2c97e95_fk_accelerator_industry_id` FOREIGN KEY (`parent_id`) REFERENCES `accelerator_industry` (`id`);
CREATE INDEX `accelerator_industry_caf7cc51` ON `accelerator_industry` (`lft`);
CREATE INDEX `accelerator_industry_3cfbd988` ON `accelerator_industry` (`rght`);
CREATE INDEX `accelerator_industry_656442a0` ON `accelerator_industry` (`tree_id`);
CREATE INDEX `accelerator_industry_c9e9a848` ON `accelerator_industry` (`level`);
CREATE INDEX `accelerator_industry_6be37982` ON `accelerator_industry` (`parent_id`);
ALTER TABLE `accelerator_startup` ADD CONSTRAINT `accelerator_star_currency_id_10b3dc69_fk_accelerator_currency_id` FOREIGN KEY (`currency_id`) REFERENCES `accelerator_currency` (`id`);
ALTER TABLE `accelerator_startup` ADD CONSTRAINT `accelera_organization_id_73b3991c_fk_accelerator_organization_id` FOREIGN KEY (`organization_id`) REFERENCES `accelerator_organization` (`id`);
ALTER TABLE `accelerator_startup` ADD CONSTRAINT `accelera_primary_industry_id_eb49739b_fk_accelerator_industry_id` FOREIGN KEY (`primary_industry_id`) REFERENCES `accelerator_industry` (`id`);
ALTER TABLE `accelerator_startup` ADD CONSTRAINT `accelerator_startup_user_id_e5e4c56a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_startup_related_industry` ADD CONSTRAINT `accelerator_startu_startup_id_c3f51826_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startup_related_industry` ADD CONSTRAINT `accelerator_star_industry_id_e7aad4a2_fk_accelerator_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `accelerator_industry` (`id`);
ALTER TABLE `accelerator_startup_related_industry` ADD CONSTRAINT `accelerator_startup_related_industry_startup_id_3dfc61dd_uniq` UNIQUE (`startup_id`, `industry_id`);
ALTER TABLE `accelerator_startup_recommendation_tags` ADD CONSTRAINT `accelerator_startu_startup_id_7481c218_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startup_recommendation_tags` ADD CONSTRAINT `e56e391f0d95f4e4f86ff0c350ba7e67` FOREIGN KEY (`recommendationtag_id`) REFERENCES `accelerator_recommendationtag` (`id`);
ALTER TABLE `accelerator_startup_recommendation_tags` ADD CONSTRAINT `accelerator_startup_recommendation_tags_startup_id_9f3106bb_uniq` UNIQUE (`startup_id`, `recommendationtag_id`);
CREATE INDEX `accelerator_jobposting_99f77c8c` ON `accelerator_jobposting` (`startup_id`);
ALTER TABLE `accelerator_jobposting` ADD CONSTRAINT `accelerator_jobpos_startup_id_5b8063be_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_applicationanswer` ADD CONSTRAINT `accelerato_application_id_b771cf55_fk_accelerator_application_id` FOREIGN KEY (`application_id`) REFERENCES `accelerator_application` (`id`);
ALTER TABLE `accelerator_programcycle` ADD CONSTRAINT `D33b237f547b7acc0010c8ade8df6f39` FOREIGN KEY (`default_application_type_id`) REFERENCES `accelerator_applicationtype` (`id`);
ALTER TABLE `accelerator_programcycle` ADD CONSTRAINT `D13b92be3a14ce323f50cedb38016bda` FOREIGN KEY (`default_overview_application_type_id`) REFERENCES `accelerator_applicationtype` (`id`);
ALTER TABLE `accelerator_startuplabel_startups` ADD CONSTRAINT `accelera_startuplabel_id_9461addd_fk_accelerator_startuplabel_id` FOREIGN KEY (`startuplabel_id`) REFERENCES `accelerator_startuplabel` (`id`);
ALTER TABLE `accelerator_startuplabel_startups` ADD CONSTRAINT `accelerator_startu_startup_id_e90b9b39_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startuplabel_startups` ADD CONSTRAINT `accelerator_startuplabel_startups_startuplabel_id_a9e72832_uniq` UNIQUE (`startuplabel_id`, `startup_id`);
CREATE INDEX `accelerator_program_d7b272e0` ON `accelerator_program` (`cycle_id`);
ALTER TABLE `accelerator_program` ADD CONSTRAINT `accelerator_pro_cycle_id_82214972_fk_accelerator_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `accelerator_programcycle` (`id`);
CREATE INDEX `accelerator_program_6c161578` ON `accelerator_program` (`mentor_program_group_id`);
ALTER TABLE `accelerator_program` ADD CONSTRAINT `ac_mentor_program_group_id_c44df547_fk_accelerator_namedgroup_id` FOREIGN KEY (`mentor_program_group_id`) REFERENCES `accelerator_namedgroup` (`id`);
CREATE INDEX `accelerator_program_4645df85` ON `accelerator_program` (`program_family_id`);
ALTER TABLE `accelerator_program` ADD CONSTRAINT `accel_program_family_id_a9b8c880_fk_accelerator_programfamily_id` FOREIGN KEY (`program_family_id`) REFERENCES `accelerator_programfamily` (`id`);
CREATE INDEX `accelerator_applicationtype_fcd6cf16` ON `accelerator_applicationtype` (`submission_label_id`);
ALTER TABLE `accelerator_applicationtype` ADD CONSTRAINT `acce_submission_label_id_499c9a6d_fk_accelerator_startuplabel_id` FOREIGN KEY (`submission_label_id`) REFERENCES `accelerator_startuplabel` (`id`);
CREATE INDEX `accelerator_applicationquestion_41d946db` ON `accelerator_applicationquestion` (`application_type_id`);
ALTER TABLE `accelerator_applicationquestion` ADD CONSTRAINT `a_application_type_id_c1c3a702_fk_accelerator_applicationtype_id` FOREIGN KEY (`application_type_id`) REFERENCES `accelerator_applicationtype` (`id`);
CREATE INDEX `accelerator_applicationquestion_429b1823` ON `accelerator_applicationquestion` (`program_id`);
ALTER TABLE `accelerator_applicationquestion` ADD CONSTRAINT `accelerator_applic_program_id_544441d7_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
CREATE INDEX `accelerator_applicationquestion_7aa0f6ee` ON `accelerator_applicationquestion` (`question_id`);
ALTER TABLE `accelerator_applicationquestion` ADD CONSTRAINT `accelerator_appl_question_id_e0664613_fk_accelerator_question_id` FOREIGN KEY (`question_id`) REFERENCES `accelerator_question` (`id`);
CREATE INDEX `accelerator_applicationanswer_5a14aa43` ON `accelerator_applicationanswer` (`application_question_id`);
ALTER TABLE `accelerator_applicationanswer` ADD CONSTRAINT `D7e8d11c870e936b8e8cb1872825922a` FOREIGN KEY (`application_question_id`) REFERENCES `accelerator_applicationquestion` (`id`);
CREATE INDEX `accelerator_application_41d946db` ON `accelerator_application` (`application_type_id`);
ALTER TABLE `accelerator_application` ADD CONSTRAINT `a_application_type_id_198546d9_fk_accelerator_applicationtype_id` FOREIGN KEY (`application_type_id`) REFERENCES `accelerator_applicationtype` (`id`);
CREATE INDEX `accelerator_application_d7b272e0` ON `accelerator_application` (`cycle_id`);
ALTER TABLE `accelerator_application` ADD CONSTRAINT `accelerator_app_cycle_id_67f1dd23_fk_accelerator_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `accelerator_programcycle` (`id`);
CREATE INDEX `accelerator_application_99f77c8c` ON `accelerator_application` (`startup_id`);
ALTER TABLE `accelerator_application` ADD CONSTRAINT `accelerator_applic_startup_id_e30524c0_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_applicationpanelassignment` ADD CONSTRAINT `accelerato_application_id_9869485b_fk_accelerator_application_id` FOREIGN KEY (`application_id`) REFERENCES `accelerator_application` (`id`);
ALTER TABLE `accelerator_bucketstate` ADD CONSTRAINT `accelerator_buc_cycle_id_2e3459c0_fk_accelerator_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `accelerator_programcycle` (`id`);
ALTER TABLE `accelerator_clearance` ADD CONSTRAINT `accel_program_family_id_d254a3b3_fk_accelerator_programfamily_id` FOREIGN KEY (`program_family_id`) REFERENCES `accelerator_programfamily` (`id`);
ALTER TABLE `accelerator_clearance` ADD CONSTRAINT `accelerator_clearance_user_id_6712d50e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_entrepreneurprofile` ADD CONSTRAINT `accelerato_current_program_id_74044f0a_fk_accelerator_program_id` FOREIGN KEY (`current_program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_functionalexpertise` ADD CONSTRAINT `acceler_parent_id_590e8e95_fk_accelerator_functionalexpertise_id` FOREIGN KEY (`parent_id`) REFERENCES `accelerator_functionalexpertise` (`id`);
CREATE INDEX `accelerator_functionalexpertise_caf7cc51` ON `accelerator_functionalexpertise` (`lft`);
CREATE INDEX `accelerator_functionalexpertise_3cfbd988` ON `accelerator_functionalexpertise` (`rght`);
CREATE INDEX `accelerator_functionalexpertise_656442a0` ON `accelerator_functionalexpertise` (`tree_id`);
CREATE INDEX `accelerator_functionalexpertise_c9e9a848` ON `accelerator_functionalexpertise` (`level`);
CREATE INDEX `accelerator_functionalexpertise_6be37982` ON `accelerator_functionalexpertise` (`parent_id`);
ALTER TABLE `accelerator_interestcategory` ADD CONSTRAINT `accelerator_intere_program_id_97bf5cb1_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_judgeapplicationfeedback` ADD CONSTRAINT `accelerato_application_id_29d5672d_fk_accelerator_application_id` FOREIGN KEY (`application_id`) REFERENCES `accelerator_application` (`id`);
ALTER TABLE `accelerator_judgepanelassignment` ADD CONSTRAINT `accelerator_judgepanelassignme_judge_id_eee979eb_fk_auth_user_id` FOREIGN KEY (`judge_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_judgeroundcommitment` ADD CONSTRAINT `accelerator_judgeroundcommitme_judge_id_beda4b2f_fk_auth_user_id` FOREIGN KEY (`judge_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_judgingformelement` ADD CONSTRAINT `a4054f3c040212bc8faf8eb5bf3962f5` FOREIGN KEY (`application_question_id`) REFERENCES `accelerator_applicationquestion` (`id`);
ALTER TABLE `accelerator_judgingformelement` ADD CONSTRAINT `accelerator__form_type_id_f0f0b855_fk_accelerator_judgingform_id` FOREIGN KEY (`form_type_id`) REFERENCES `accelerator_judgingform` (`id`);
ALTER TABLE `accelerator_judginground` ADD CONSTRAINT `a_application_type_id_69059c57_fk_accelerator_applicationtype_id` FOREIGN KEY (`application_type_id`) REFERENCES `accelerator_applicationtype` (`id`);
ALTER TABLE `accelerator_memberprofile` ADD CONSTRAINT `accelerato_current_program_id_f6538fd3_fk_accelerator_program_id` FOREIGN KEY (`current_program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_memberprofile` ADD CONSTRAINT `accelerator_memberprofile_user_id_1ee08fa8_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_memberprofile_interest_categories` ADD CONSTRAINT `accele_memberprofile_id_b9c3b5ae_fk_accelerator_memberprofile_id` FOREIGN KEY (`memberprofile_id`) REFERENCES `accelerator_memberprofile` (`id`);
ALTER TABLE `accelerator_memberprofile_interest_categories` ADD CONSTRAINT `interestcategory_id_cc9c6ee4_fk_accelerator_interestcategory_id` FOREIGN KEY (`interestcategory_id`) REFERENCES `accelerator_interestcategory` (`id`);
ALTER TABLE `accelerator_memberprofile_interest_categories` ADD CONSTRAINT `accelerator_memberprofile_interes_memberprofile_id_c2e35c5a_uniq` UNIQUE (`memberprofile_id`, `interestcategory_id`);
ALTER TABLE `accelerator_memberprofile_program_families` ADD CONSTRAINT `accele_memberprofile_id_3639d592_fk_accelerator_memberprofile_id` FOREIGN KEY (`memberprofile_id`) REFERENCES `accelerator_memberprofile` (`id`);
ALTER TABLE `accelerator_memberprofile_program_families` ADD CONSTRAINT `accele_programfamily_id_1082beda_fk_accelerator_programfamily_id` FOREIGN KEY (`programfamily_id`) REFERENCES `accelerator_programfamily` (`id`);
ALTER TABLE `accelerator_memberprofile_program_families` ADD CONSTRAINT `accelerator_memberprofile_program_memberprofile_id_e094f435_uniq` UNIQUE (`memberprofile_id`, `programfamily_id`);
ALTER TABLE `accelerator_memberprofile_recommendation_tags` ADD CONSTRAINT `accele_memberprofile_id_a23949c5_fk_accelerator_memberprofile_id` FOREIGN KEY (`memberprofile_id`) REFERENCES `accelerator_memberprofile` (`id`);
ALTER TABLE `accelerator_memberprofile_recommendation_tags` ADD CONSTRAINT `b462b5c4ff24d4b8f5d6032191914bc3` FOREIGN KEY (`recommendationtag_id`) REFERENCES `accelerator_recommendationtag` (`id`);
ALTER TABLE `accelerator_memberprofile_recommendation_tags` ADD CONSTRAINT `accelerator_memberprofile_recomme_memberprofile_id_4fad2f4b_uniq` UNIQUE (`memberprofile_id`, `recommendationtag_id`);
ALTER TABLE `accelerator_mentorprogramofficehour` ADD CONSTRAINT `accelerator_mentorprogramof_finalist_id_753752bf_fk_auth_user_id` FOREIGN KEY (`finalist_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_mentorprogramofficehour` ADD CONSTRAINT `accelerator_mentorprogramoffi_mentor_id_4d40039a_fk_auth_user_id` FOREIGN KEY (`mentor_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_mentorprogramofficehour` ADD CONSTRAINT `accelerator_mentor_program_id_7bd22248_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
CREATE INDEX `accelerator_mentorprogramofficehour_5fc73231` ON `accelerator_mentorprogramofficehour` (`date`);
CREATE INDEX `accelerator_mentorprogramofficehour_c4d98dbd` ON `accelerator_mentorprogramofficehour` (`start_time`);
CREATE INDEX `accelerator_mentorprogramofficehour_305d2889` ON `accelerator_mentorprogramofficehour` (`end_time`);
ALTER TABLE `accelerator_newsletter` ADD CONSTRAINT `acceler_judging_round_id_1033a046_fk_accelerator_judginground_id` FOREIGN KEY (`judging_round_id`) REFERENCES `accelerator_judginground` (`id`);
ALTER TABLE `accelerator_newsletter` ADD CONSTRAINT `accelerator_newsle_program_id_15e39d9f_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_newsletterreceipt` ADD CONSTRAINT `accelerator__newsletter_id_26434575_fk_accelerator_newsletter_id` FOREIGN KEY (`newsletter_id`) REFERENCES `accelerator_newsletter` (`id`);
ALTER TABLE `accelerator_newsletterreceipt` ADD CONSTRAINT `accelerator_newsletterrece_recipient_id_d50b74ed_fk_auth_user_id` FOREIGN KEY (`recipient_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_panellocation` ADD CONSTRAINT `acceler_judging_round_id_f94734b3_fk_accelerator_judginground_id` FOREIGN KEY (`judging_round_id`) REFERENCES `accelerator_judginground` (`id`);
ALTER TABLE `accelerator_paneltime` ADD CONSTRAINT `acceler_judging_round_id_71f51316_fk_accelerator_judginground_id` FOREIGN KEY (`judging_round_id`) REFERENCES `accelerator_judginground` (`id`);
ALTER TABLE `accelerator_paneltype` ADD CONSTRAINT `acceler_judging_round_id_883e88ce_fk_accelerator_judginground_id` FOREIGN KEY (`judging_round_id`) REFERENCES `accelerator_judginground` (`id`);
ALTER TABLE `accelerator_partner` ADD CONSTRAINT `accelera_organization_id_bb096079_fk_accelerator_organization_id` FOREIGN KEY (`organization_id`) REFERENCES `accelerator_organization` (`id`);
ALTER TABLE `accelerator_partnerteammember` ADD CONSTRAINT `accelerator_partne_partner_id_dfeb30d7_fk_accelerator_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `accelerator_partner` (`id`);
ALTER TABLE `accelerator_partnerteammember` ADD CONSTRAINT `accelerator_partnerteamm_team_member_id_c1227a94_fk_auth_user_id` FOREIGN KEY (`team_member_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_programoverride` ADD CONSTRAINT `accelerator_pro_cycle_id_f606cfda_fk_accelerator_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `accelerator_programcycle` (`id`);
ALTER TABLE `accelerator_programoverride` ADD CONSTRAINT `accelerator_progra_program_id_9fb54f92_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_programpartner` ADD CONSTRAINT `accelerator_progra_partner_id_02b85e70_fk_accelerator_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `accelerator_partner` (`id`);
ALTER TABLE `accelerator_programpartnertype` ADD CONSTRAINT `accelerator_progra_program_id_b2114b9e_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_programrole` ADD CONSTRAINT `accelerator_progra_program_id_f691f66f_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_programrolegrant` ADD CONSTRAINT `accelerator_programrolegrant_person_id_83afe265_fk_auth_user_id` FOREIGN KEY (`person_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_programrolegrant` ADD CONSTRAINT `accelerat_program_role_id_0c2d04ea_fk_accelerator_programrole_id` FOREIGN KEY (`program_role_id`) REFERENCES `accelerator_programrole` (`id`);
ALTER TABLE `accelerator_programstartupattribute` ADD CONSTRAINT `accelerator_progra_program_id_e5142815_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_programstartupstatus` ADD CONSTRAINT `accelerator_progra_program_id_31bce7ba_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_refundcode` ADD CONSTRAINT `accelerator_refu_issued_to_id_2063162e_fk_accelerator_partner_id` FOREIGN KEY (`issued_to_id`) REFERENCES `accelerator_partner` (`id`);
ALTER TABLE `accelerator_refundcode_programs` ADD CONSTRAINT `accelerator__refundcode_id_a3f04c03_fk_accelerator_refundcode_id` FOREIGN KEY (`refundcode_id`) REFERENCES `accelerator_refundcode` (`id`);
ALTER TABLE `accelerator_refundcode_programs` ADD CONSTRAINT `accelerator_refund_program_id_b17dc915_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_refundcode_programs` ADD CONSTRAINT `accelerator_refundcode_programs_refundcode_id_1789eeed_uniq` UNIQUE (`refundcode_id`, `program_id`);
ALTER TABLE `accelerator_refundcoderedemption` ADD CONSTRAINT `accelerator_ref_cycle_id_de8d1b4b_fk_accelerator_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `accelerator_programcycle` (`id`);
ALTER TABLE `accelerator_refundcoderedemption` ADD CONSTRAINT `accelerator_refund_code_id_7e6d1d76_fk_accelerator_refundcode_id` FOREIGN KEY (`refund_code_id`) REFERENCES `accelerator_refundcode` (`id`);
ALTER TABLE `accelerator_refundcoderedemption` ADD CONSTRAINT `accelerator_refund_startup_id_ce506a88_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_scenarioapplication` ADD CONSTRAINT `accelerato_application_id_2893c306_fk_accelerator_application_id` FOREIGN KEY (`application_id`) REFERENCES `accelerator_application` (`id`);
ALTER TABLE `accelerator_scenarioapplication` ADD CONSTRAINT `accelerator_scen_scenario_id_f364bf38_fk_accelerator_scenario_id` FOREIGN KEY (`scenario_id`) REFERENCES `accelerator_scenario` (`id`);
ALTER TABLE `accelerator_scenariojudge` ADD CONSTRAINT `accelerator_scenariojudge_judge_id_1f7f909c_fk_auth_user_id` FOREIGN KEY (`judge_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_scenariojudge` ADD CONSTRAINT `accelerator_scen_scenario_id_52c1bbe8_fk_accelerator_scenario_id` FOREIGN KEY (`scenario_id`) REFERENCES `accelerator_scenario` (`id`);
ALTER TABLE `accelerator_scenariopreference` ADD CONSTRAINT `accelerator_scen_scenario_id_2de733b7_fk_accelerator_scenario_id` FOREIGN KEY (`scenario_id`) REFERENCES `accelerator_scenario` (`id`);
ALTER TABLE `accelerator_section` ADD CONSTRAINT `accelerator__newsletter_id_a942ee9a_fk_accelerator_newsletter_id` FOREIGN KEY (`newsletter_id`) REFERENCES `accelerator_newsletter` (`id`);
ALTER TABLE `accelerator_section_interest_categories` ADD CONSTRAINT `accelerator_sectio_section_id_9bc17408_fk_accelerator_section_id` FOREIGN KEY (`section_id`) REFERENCES `accelerator_section` (`id`);
ALTER TABLE `accelerator_section_interest_categories` ADD CONSTRAINT `interestcategory_id_caa54dd3_fk_accelerator_interestcategory_id` FOREIGN KEY (`interestcategory_id`) REFERENCES `accelerator_interestcategory` (`id`);
ALTER TABLE `accelerator_section_interest_categories` ADD CONSTRAINT `accelerator_section_interest_categories_section_id_a8f4a518_uniq` UNIQUE (`section_id`, `interestcategory_id`);
ALTER TABLE `accelerator_siteprogramauthorization` ADD CONSTRAINT `accelerator_sitepr_program_id_4786621d_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_siteprogramauthorization` ADD CONSTRAINT `accelerator_siteprograma_site_id_fb8dbeba_fk_accelerator_site_id` FOREIGN KEY (`site_id`) REFERENCES `accelerator_site` (`id`);
ALTER TABLE `accelerator_startupattribute` ADD CONSTRAINT `attribute_id_52e1a312_fk_accelerator_programstartupattribute_id` FOREIGN KEY (`attribute_id`) REFERENCES `accelerator_programstartupattribute` (`id`);
ALTER TABLE `accelerator_startupattribute` ADD CONSTRAINT `accelerator_startu_startup_id_647793cd_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startupcycleinterest` ADD CONSTRAINT `accelerator_sta_cycle_id_5b5fb5ec_fk_accelerator_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `accelerator_programcycle` (`id`);
ALTER TABLE `accelerator_startupmentorrelationship` ADD CONSTRAINT `accelerator_startupmentorrela_mentor_id_1a46af5e_fk_auth_user_id` FOREIGN KEY (`mentor_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_startupmentortrackingrecord` ADD CONSTRAINT `accelerator_startu_program_id_934066e4_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_startupmentortrackingrecord` ADD CONSTRAINT `accelerator_startu_startup_id_2ccec7c6_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startupoverridegrant` ADD CONSTRAINT `a_program_override_id_22bcfce3_fk_accelerator_programoverride_id` FOREIGN KEY (`program_override_id`) REFERENCES `accelerator_programoverride` (`id`);
ALTER TABLE `accelerator_startupoverridegrant` ADD CONSTRAINT `accelerator_startu_startup_id_6ebf355a_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startupprograminterest` ADD CONSTRAINT `accelerator_startu_program_id_958ea568_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `accelerator_startupprograminterest` ADD CONSTRAINT `accelerator_startu_startup_id_5739e1f2_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startupprograminterest` ADD CONSTRAINT `D367c025886bd8ad074610720e7d9a0f` FOREIGN KEY (`startup_cycle_interest_id`) REFERENCES `accelerator_startupcycleinterest` (`id`);
CREATE INDEX `accelerator_startupprograminterest_70a17ffa` ON `accelerator_startupprograminterest` (`order`);
ALTER TABLE `accelerator_startupstatus` ADD CONSTRAINT `badb878861b20ff99252ece038236120` FOREIGN KEY (`program_startup_status_id`) REFERENCES `accelerator_programstartupstatus` (`id`);
ALTER TABLE `accelerator_startupstatus` ADD CONSTRAINT `accelerator_startu_startup_id_89b7a36b_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startupteammember` ADD CONSTRAINT `accelerator_startu_startup_id_e9a95802_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_startupteammember` ADD CONSTRAINT `accelerator_startupteammember_user_id_2a4bf06c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_startupteammember_recommendation_tags` ADD CONSTRAINT `d8492bb29042c620a729fe91aadcad09` FOREIGN KEY (`startupteammember_id`) REFERENCES `accelerator_startupteammember` (`id`);
ALTER TABLE `accelerator_startupteammember_recommendation_tags` ADD CONSTRAINT `D5988efc189eb9d51ed24a44e2f4104c` FOREIGN KEY (`recommendationtag_id`) REFERENCES `accelerator_recommendationtag` (`id`);
ALTER TABLE `accelerator_startupteammember_recommendation_tags` ADD CONSTRAINT `accelerator_startupteammember_startupteammember_id_ee715769_uniq` UNIQUE (`startupteammember_id`, `recommendationtag_id`);
ALTER TABLE `accelerator_userlabel_users` ADD CONSTRAINT `accelerator_us_userlabel_id_0f5b3bc8_fk_accelerator_userlabel_id` FOREIGN KEY (`userlabel_id`) REFERENCES `accelerator_userlabel` (`id`);
ALTER TABLE `accelerator_userlabel_users` ADD CONSTRAINT `accelerator_userlabel_users_user_id_ca08396f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_userlabel_users` ADD CONSTRAINT `accelerator_userlabel_users_userlabel_id_2ce6de54_uniq` UNIQUE (`userlabel_id`, `user_id`);
ALTER TABLE `accelerator_paypalpayment` ADD CONSTRAINT `accelerator_pay_cycle_id_983d4615_fk_accelerator_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `accelerator_programcycle` (`id`);
ALTER TABLE `accelerator_paypalpayment` ADD CONSTRAINT `accelerator_paypal_startup_id_219895ec_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
ALTER TABLE `accelerator_baseprofile` ADD CONSTRAINT `accelerator_baseprofile_user_id_ae20d832_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_reference` ADD CONSTRAINT `accelerato_application_id_6f6628e1_fk_accelerator_application_id` FOREIGN KEY (`application_id`) REFERENCES `accelerator_application` (`id`);
ALTER TABLE `accelerator_reference` ADD CONSTRAINT `accelerator_referenc_requesting_user_id_1b81a238_fk_auth_user_id` FOREIGN KEY (`requesting_user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `pagetype_accelerator_userrolemenu` ADD CONSTRAINT `pagetype_acce_urlnode_ptr_id_1aa1b4b8_fk_fluent_pages_urlnode_id` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`);
ALTER TABLE `pagetype_accelerator_userrolemenu` ADD CONSTRAINT `pagetype_accelerat_program_id_5b872aec_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
ALTER TABLE `pagetype_accelerator_userrolemenu` ADD CONSTRAINT `paget_program_family_id_394089ba_fk_accelerator_programfamily_id` FOREIGN KEY (`program_family_id`) REFERENCES `accelerator_programfamily` (`id`);
ALTER TABLE `pagetype_accelerator_userrolemenu` ADD CONSTRAINT `pagetype_accele_user_role_id_c9d2ef19_fk_accelerator_userrole_id` FOREIGN KEY (`user_role_id`) REFERENCES `accelerator_userrole` (`id`);
ALTER TABLE `pagetype_accelerator_categoryheaderpage` ADD CONSTRAINT `pagetype_acce_urlnode_ptr_id_f671351e_fk_fluent_pages_urlnode_id` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`);
ALTER TABLE `pagetype_accelerator_filepage` ADD CONSTRAINT `pagetype_acce_urlnode_ptr_id_2de9f027_fk_fluent_pages_urlnode_id` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`);
ALTER TABLE `accelerator_nodepublishedfor` ADD CONSTRAINT `accelerator_nodepubl_node_id_85421ea1_fk_fluent_pages_urlnode_id` FOREIGN KEY (`node_id`) REFERENCES `fluent_pages_urlnode` (`id`);
ALTER TABLE `accelerator_nodepublishedfor` ADD CONSTRAINT `accelera_published_for_id_f2a320f1_fk_accelerator_programrole_id` FOREIGN KEY (`published_for_id`) REFERENCES `accelerator_programrole` (`id`);
ALTER TABLE `accelerator_expertinterest` ADD CONSTRAINT `a_interest_type_id_4d5bcc31_fk_accelerator_expertinteresttype_id` FOREIGN KEY (`interest_type_id`) REFERENCES `accelerator_expertinteresttype` (`id`);
ALTER TABLE `accelerator_expertinterest` ADD CONSTRAINT `accel_program_family_id_ffc7a168_fk_accelerator_programfamily_id` FOREIGN KEY (`program_family_id`) REFERENCES `accelerator_programfamily` (`id`);
ALTER TABLE `accelerator_expertinterest` ADD CONSTRAINT `accelerator_expertinterest_user_id_353b4949_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `pagetype_accelerator_siteredirectpage` ADD CONSTRAINT `pagetype_acce_urlnode_ptr_id_2ab229ad_fk_fluent_pages_urlnode_id` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`);
CREATE INDEX `accelerator_startupmentorrelationship_48222c2b` ON `accelerator_startupmentorrelationship` (`startup_mentor_tracking_id`);
ALTER TABLE `accelerator_startupmentorrelationship` ADD CONSTRAINT `bf7ebdd899654107db7c30d7987754a0` FOREIGN KEY (`startup_mentor_tracking_id`) REFERENCES `accelerator_startupmentortrackingrecord` (`id`);
CREATE INDEX `accelerator_startupcycleinterest_99f77c8c` ON `accelerator_startupcycleinterest` (`startup_id`);
ALTER TABLE `accelerator_startupcycleinterest` ADD CONSTRAINT `accelerator_startu_startup_id_832e7a62_fk_accelerator_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `accelerator_startup` (`id`);
CREATE INDEX `accelerator_scenario_0cc25dbd` ON `accelerator_scenario` (`judging_round_id`);
ALTER TABLE `accelerator_scenario` ADD CONSTRAINT `acceler_judging_round_id_0cb4e507_fk_accelerator_judginground_id` FOREIGN KEY (`judging_round_id`) REFERENCES `accelerator_judginground` (`id`);
CREATE INDEX `accelerator_programstartupstatus_5f4af245` ON `accelerator_programstartupstatus` (`startup_role_id`);
ALTER TABLE `accelerator_programstartupstatus` ADD CONSTRAINT `accelerat_startup_role_id_158d0bd0_fk_accelerator_startuprole_id` FOREIGN KEY (`startup_role_id`) REFERENCES `accelerator_startuprole` (`id`);
CREATE INDEX `accelerator_programrole_75df8002` ON `accelerator_programrole` (`user_label_id`);
ALTER TABLE `accelerator_programrole` ADD CONSTRAINT `accelerator_p_user_label_id_3e80edbf_fk_accelerator_userlabel_id` FOREIGN KEY (`user_label_id`) REFERENCES `accelerator_userlabel` (`id`);
CREATE INDEX `accelerator_programrole_1728abaf` ON `accelerator_programrole` (`user_role_id`);
ALTER TABLE `accelerator_programrole` ADD CONSTRAINT `accelerator_pro_user_role_id_9fd14dba_fk_accelerator_userrole_id` FOREIGN KEY (`user_role_id`) REFERENCES `accelerator_userrole` (`id`);
CREATE INDEX `accelerator_programpartner_19564e43` ON `accelerator_programpartner` (`partner_type_id`);
ALTER TABLE `accelerator_programpartner` ADD CONSTRAINT `ac_partner_type_id_a7b86b33_fk_accelerator_programpartnertype_id` FOREIGN KEY (`partner_type_id`) REFERENCES `accelerator_programpartnertype` (`id`);
CREATE INDEX `accelerator_programpartner_429b1823` ON `accelerator_programpartner` (`program_id`);
ALTER TABLE `accelerator_programpartner` ADD CONSTRAINT `accelerator_progra_program_id_657d8b49_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
CREATE INDEX `accelerator_paypalrefund_376ebbba` ON `accelerator_paypalrefund` (`payment_id`);
ALTER TABLE `accelerator_paypalrefund` ADD CONSTRAINT `accelerator__payment_id_5b3c6256_fk_accelerator_paypalpayment_id` FOREIGN KEY (`payment_id`) REFERENCES `accelerator_paypalpayment` (`id`);
CREATE INDEX `accelerator_panel_e274a5da` ON `accelerator_panel` (`location_id`);
ALTER TABLE `accelerator_panel` ADD CONSTRAINT `accel_location_id_aefab2c7_fk_accelerator_panellocation_location` FOREIGN KEY (`location_id`) REFERENCES `accelerator_panellocation` (`location`);
CREATE INDEX `accelerator_panel_91d978f0` ON `accelerator_panel` (`panel_time_id`);
ALTER TABLE `accelerator_panel` ADD CONSTRAINT `accelerator_p_panel_time_id_018a9354_fk_accelerator_paneltime_id` FOREIGN KEY (`panel_time_id`) REFERENCES `accelerator_paneltime` (`id`);
CREATE INDEX `accelerator_panel_17ddce3a` ON `accelerator_panel` (`panel_type_id`);
ALTER TABLE `accelerator_panel` ADD CONSTRAINT `accel_panel_type_id_37f529bf_fk_accelerator_paneltype_panel_type` FOREIGN KEY (`panel_type_id`) REFERENCES `accelerator_paneltype` (`panel_type`);
ALTER TABLE `accelerator_observer_newsletter_cc_roles` ADD CONSTRAINT `accelerator_obse_observer_id_97dea6d8_fk_accelerator_observer_id` FOREIGN KEY (`observer_id`) REFERENCES `accelerator_observer` (`id`);
ALTER TABLE `accelerator_observer_newsletter_cc_roles` ADD CONSTRAINT `accelerato_programrole_id_8748a2f7_fk_accelerator_programrole_id` FOREIGN KEY (`programrole_id`) REFERENCES `accelerator_programrole` (`id`);
ALTER TABLE `accelerator_observer_newsletter_cc_roles` ADD CONSTRAINT `accelerator_observer_newsletter_cc_rol_observer_id_0245f832_uniq` UNIQUE (`observer_id`, `programrole_id`);
ALTER TABLE `accelerator_newsletter_recipient_roles` ADD CONSTRAINT `accelerator__newsletter_id_b0aa837c_fk_accelerator_newsletter_id` FOREIGN KEY (`newsletter_id`) REFERENCES `accelerator_newsletter` (`id`);
ALTER TABLE `accelerator_newsletter_recipient_roles` ADD CONSTRAINT `accelerato_programrole_id_7ba63ded_fk_accelerator_programrole_id` FOREIGN KEY (`programrole_id`) REFERENCES `accelerator_programrole` (`id`);
ALTER TABLE `accelerator_newsletter_recipient_roles` ADD CONSTRAINT `accelerator_newsletter_recipient_rol_newsletter_id_b296f57f_uniq` UNIQUE (`newsletter_id`, `programrole_id`);
CREATE INDEX `accelerator_judginground_bdf8c73e` ON `accelerator_judginground` (`confirmed_judge_label_id`);
ALTER TABLE `accelerator_judginground` ADD CONSTRAINT `ac_confirmed_judge_label_id_393a4487_fk_accelerator_userlabel_id` FOREIGN KEY (`confirmed_judge_label_id`) REFERENCES `accelerator_userlabel` (`id`);
CREATE INDEX `accelerator_judginground_413c41b4` ON `accelerator_judginground` (`desired_judge_label_id`);
ALTER TABLE `accelerator_judginground` ADD CONSTRAINT `acce_desired_judge_label_id_cbb6f66e_fk_accelerator_userlabel_id` FOREIGN KEY (`desired_judge_label_id`) REFERENCES `accelerator_userlabel` (`id`);
CREATE INDEX `accelerator_judginground_b47c34bd` ON `accelerator_judginground` (`feedback_merge_with_id`);
ALTER TABLE `accelerator_judginground` ADD CONSTRAINT `a_feedback_merge_with_id_e91a44d8_fk_accelerator_judginground_id` FOREIGN KEY (`feedback_merge_with_id`) REFERENCES `accelerator_judginground` (`id`);
CREATE INDEX `accelerator_judginground_f8390639` ON `accelerator_judginground` (`judging_form_id`);
ALTER TABLE `accelerator_judginground` ADD CONSTRAINT `accelerat_judging_form_id_49398283_fk_accelerator_judgingform_id` FOREIGN KEY (`judging_form_id`) REFERENCES `accelerator_judgingform` (`id`);
CREATE INDEX `accelerator_judginground_429b1823` ON `accelerator_judginground` (`program_id`);
ALTER TABLE `accelerator_judginground` ADD CONSTRAINT `accelerator_judgin_program_id_cf976c74_fk_accelerator_program_id` FOREIGN KEY (`program_id`) REFERENCES `accelerator_program` (`id`);
CREATE INDEX `accelerator_judginground_5926436d` ON `accelerator_judginground` (`startup_label_id`);
ALTER TABLE `accelerator_judginground` ADD CONSTRAINT `acceler_startup_label_id_a26368b5_fk_accelerator_startuplabel_id` FOREIGN KEY (`startup_label_id`) REFERENCES `accelerator_startuplabel` (`id`);
CREATE INDEX `accelerator_judgeroundcommitment_0cc25dbd` ON `accelerator_judgeroundcommitment` (`judging_round_id`);
ALTER TABLE `accelerator_judgeroundcommitment` ADD CONSTRAINT `acceler_judging_round_id_3f385840_fk_accelerator_judginground_id` FOREIGN KEY (`judging_round_id`) REFERENCES `accelerator_judginground` (`id`);
CREATE INDEX `accelerator_judgepanelassignment_3be65887` ON `accelerator_judgepanelassignment` (`panel_id`);
ALTER TABLE `accelerator_judgepanelassignment` ADD CONSTRAINT `accelerator_judgepanel_panel_id_c20f50b2_fk_accelerator_panel_id` FOREIGN KEY (`panel_id`) REFERENCES `accelerator_panel` (`id`);
CREATE INDEX `accelerator_judgepanelassignment_adc0676c` ON `accelerator_judgepanelassignment` (`scenario_id`);
ALTER TABLE `accelerator_judgepanelassignment` ADD CONSTRAINT `accelerator_judg_scenario_id_1fcbf62a_fk_accelerator_scenario_id` FOREIGN KEY (`scenario_id`) REFERENCES `accelerator_scenario` (`id`);
CREATE INDEX `accelerator_judgefeedbackcomponent_f5009aa9` ON `accelerator_judgefeedbackcomponent` (`feedback_element_id`);
ALTER TABLE `accelerator_judgefeedbackcomponent` ADD CONSTRAINT `D9e0a7f8a0ac0c537099efffd5773a00` FOREIGN KEY (`feedback_element_id`) REFERENCES `accelerator_judgingformelement` (`id`);
CREATE INDEX `accelerator_judgefeedbackcomponent_7aad45f7` ON `accelerator_judgefeedbackcomponent` (`judge_feedback_id`);
ALTER TABLE `accelerator_judgefeedbackcomponent` ADD CONSTRAINT `dbe823f8b23409e28475c190848039c8` FOREIGN KEY (`judge_feedback_id`) REFERENCES `accelerator_judgeapplicationfeedback` (`id`);
CREATE INDEX `accelerator_judgeavailability_065ade21` ON `accelerator_judgeavailability` (`commitment_id`);
ALTER TABLE `accelerator_judgeavailability` ADD CONSTRAINT `ac_commitment_id_967c5406_fk_accelerator_judgeroundcommitment_id` FOREIGN KEY (`commitment_id`) REFERENCES `accelerator_judgeroundcommitment` (`id`);
CREATE INDEX `accelerator_judgeavailability_94d8985c` ON `accelerator_judgeavailability` (`panel_location_id`);
ALTER TABLE `accelerator_judgeavailability` ADD CONSTRAINT `D3aea853e5c1d5c05d6a1c4c1fc4ef77` FOREIGN KEY (`panel_location_id`) REFERENCES `accelerator_panellocation` (`location`);
CREATE INDEX `accelerator_judgeavailability_91d978f0` ON `accelerator_judgeavailability` (`panel_time_id`);
ALTER TABLE `accelerator_judgeavailability` ADD CONSTRAINT `accelerator_j_panel_time_id_3ced8165_fk_accelerator_paneltime_id` FOREIGN KEY (`panel_time_id`) REFERENCES `accelerator_paneltime` (`id`);
CREATE INDEX `accelerator_judgeavailability_17ddce3a` ON `accelerator_judgeavailability` (`panel_type_id`);
ALTER TABLE `accelerator_judgeavailability` ADD CONSTRAINT `accel_panel_type_id_94b4a433_fk_accelerator_paneltype_panel_type` FOREIGN KEY (`panel_type_id`) REFERENCES `accelerator_paneltype` (`panel_type`);
CREATE INDEX `accelerator_judgeapplicationfeedback_71f5cb07` ON `accelerator_judgeapplicationfeedback` (`form_type_id`);
ALTER TABLE `accelerator_judgeapplicationfeedback` ADD CONSTRAINT `accelerator__form_type_id_6472e1e3_fk_accelerator_judgingform_id` FOREIGN KEY (`form_type_id`) REFERENCES `accelerator_judgingform` (`id`);
CREATE INDEX `accelerator_judgeapplicationfeedback_e7c5d788` ON `accelerator_judgeapplicationfeedback` (`judge_id`);
ALTER TABLE `accelerator_judgeapplicationfeedback` ADD CONSTRAINT `accelerator_judgeapplicationfe_judge_id_75e483da_fk_auth_user_id` FOREIGN KEY (`judge_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `accelerator_judgeapplicationfeedback_3be65887` ON `accelerator_judgeapplicationfeedback` (`panel_id`);
ALTER TABLE `accelerator_judgeapplicationfeedback` ADD CONSTRAINT `accelerator_judgeappli_panel_id_dcad7a6e_fk_accelerator_panel_id` FOREIGN KEY (`panel_id`) REFERENCES `accelerator_panel` (`id`);
ALTER TABLE `accelerator_judgeapplicationfeedback_viewers` ADD CONSTRAINT `D2bf0309db3230b97596fbde829ae8cd` FOREIGN KEY (`judgeapplicationfeedback_id`) REFERENCES `accelerator_judgeapplicationfeedback` (`id`);
ALTER TABLE `accelerator_judgeapplicationfeedback_viewers` ADD CONSTRAINT `accelerator_judgeapplicationfee_user_id_255141e1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_judgeapplicationfeedback_viewers` ADD CONSTRAINT `accelerator_judgeappli_judgeapplicationfeedback_id_2764b5b8_uniq` UNIQUE (`judgeapplicationfeedback_id`, `user_id`);
ALTER TABLE `accelerator_expert_related_industry` ADD CONSTRAINT `accele_expertprofile_id_0a74b486_fk_accelerator_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `accelerator_expertprofile` (`id`);
ALTER TABLE `accelerator_expert_related_industry` ADD CONSTRAINT `accelerator_expe_industry_id_50cf2e40_fk_accelerator_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `accelerator_industry` (`id`);
ALTER TABLE `accelerator_expert_related_industry` ADD CONSTRAINT `accelerator_expert_related_indust_expertprofile_id_28efe7d7_uniq` UNIQUE (`expertprofile_id`, `industry_id`);
CREATE INDEX `accelerator_expertprofile_5a48468e` ON `accelerator_expertprofile` (`current_program_id`);
ALTER TABLE `accelerator_expertprofile` ADD CONSTRAINT `accelerato_current_program_id_9121d2a0_fk_accelerator_program_id` FOREIGN KEY (`current_program_id`) REFERENCES `accelerator_program` (`id`);
CREATE INDEX `accelerator_expertprofile_12cb36c5` ON `accelerator_expertprofile` (`expert_category_id`);
ALTER TABLE `accelerator_expertprofile` ADD CONSTRAINT `acc_expert_category_id_7c6886e9_fk_accelerator_expertcategory_id` FOREIGN KEY (`expert_category_id`) REFERENCES `accelerator_expertcategory` (`id`);
ALTER TABLE `accelerator_expertprofile_functional_expertise` ADD CONSTRAINT `accele_expertprofile_id_ad91424f_fk_accelerator_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `accelerator_expertprofile` (`id`);
ALTER TABLE `accelerator_expertprofile_functional_expertise` ADD CONSTRAINT `D12e150412eac92477d20a3b94869047` FOREIGN KEY (`functionalexpertise_id`) REFERENCES `accelerator_functionalexpertise` (`id`);
ALTER TABLE `accelerator_expertprofile_functional_expertise` ADD CONSTRAINT `accelerator_expertprofile_functio_expertprofile_id_390b913c_uniq` UNIQUE (`expertprofile_id`, `functionalexpertise_id`);
CREATE INDEX `accelerator_expertprofile_9459abc0` ON `accelerator_expertprofile` (`home_program_family_id`);
ALTER TABLE `accelerator_expertprofile` ADD CONSTRAINT `home_program_family_id_b7c976e4_fk_accelerator_programfamily_id` FOREIGN KEY (`home_program_family_id`) REFERENCES `accelerator_programfamily` (`id`);
ALTER TABLE `accelerator_expertprofile_interest_categories` ADD CONSTRAINT `accele_expertprofile_id_84634bb0_fk_accelerator_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `accelerator_expertprofile` (`id`);
ALTER TABLE `accelerator_expertprofile_interest_categories` ADD CONSTRAINT `interestcategory_id_09d06a0e_fk_accelerator_interestcategory_id` FOREIGN KEY (`interestcategory_id`) REFERENCES `accelerator_interestcategory` (`id`);
ALTER TABLE `accelerator_expertprofile_interest_categories` ADD CONSTRAINT `accelerator_expertprofile_interes_expertprofile_id_de1dfb97_uniq` UNIQUE (`expertprofile_id`, `interestcategory_id`);
ALTER TABLE `accelerator_expert_related_mentoringspecialty` ADD CONSTRAINT `accele_expertprofile_id_16922be5_fk_accelerator_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `accelerator_expertprofile` (`id`);
ALTER TABLE `accelerator_expert_related_mentoringspecialty` ADD CONSTRAINT `D70f2d4d115e0e77baa958a119c99410` FOREIGN KEY (`mentoringspecialties_id`) REFERENCES `accelerator_mentoringspecialties` (`id`);
ALTER TABLE `accelerator_expert_related_mentoringspecialty` ADD CONSTRAINT `accelerator_expert_related_mentor_expertprofile_id_db6c6808_uniq` UNIQUE (`expertprofile_id`, `mentoringspecialties_id`);
CREATE INDEX `accelerator_expertprofile_575a44eb` ON `accelerator_expertprofile` (`primary_industry_id`);
ALTER TABLE `accelerator_expertprofile` ADD CONSTRAINT `accelera_primary_industry_id_1a6fc9f6_fk_accelerator_industry_id` FOREIGN KEY (`primary_industry_id`) REFERENCES `accelerator_industry` (`id`);
ALTER TABLE `accelerator_expertprofile_program_families` ADD CONSTRAINT `accele_expertprofile_id_b9c10d4e_fk_accelerator_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `accelerator_expertprofile` (`id`);
ALTER TABLE `accelerator_expertprofile_program_families` ADD CONSTRAINT `accele_programfamily_id_9f922f7f_fk_accelerator_programfamily_id` FOREIGN KEY (`programfamily_id`) REFERENCES `accelerator_programfamily` (`id`);
ALTER TABLE `accelerator_expertprofile_program_families` ADD CONSTRAINT `accelerator_expertprofile_program_expertprofile_id_c70161c7_uniq` UNIQUE (`expertprofile_id`, `programfamily_id`);
ALTER TABLE `accelerator_expertprofile_recommendation_tags` ADD CONSTRAINT `accele_expertprofile_id_7e7d12c2_fk_accelerator_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `accelerator_expertprofile` (`id`);
ALTER TABLE `accelerator_expertprofile_recommendation_tags` ADD CONSTRAINT `cb20706c875a5fe579b9f201729e8b63` FOREIGN KEY (`recommendationtag_id`) REFERENCES `accelerator_recommendationtag` (`id`);
ALTER TABLE `accelerator_expertprofile_recommendation_tags` ADD CONSTRAINT `accelerator_expertprofile_recomme_expertprofile_id_b2e5098b_uniq` UNIQUE (`expertprofile_id`, `recommendationtag_id`);
ALTER TABLE `accelerator_expertprofile` ADD CONSTRAINT `accelerator_expertprofile_user_id_486d104f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `accelerator_entrepreneurprofile_interest_categories` ADD CONSTRAINT `D9b93415cbf5de1b37df10051ad5854a` FOREIGN KEY (`entrepreneurprofile_id`) REFERENCES `accelerator_entrepreneurprofile` (`id`);
ALTER TABLE `accelerator_entrepreneurprofile_interest_categories` ADD CONSTRAINT `interestcategory_id_56478ebb_fk_accelerator_interestcategory_id` FOREIGN KEY (`interestcategory_id`) REFERENCES `accelerator_interestcategory` (`id`);
ALTER TABLE `accelerator_entrepreneurprofile_interest_categories` ADD CONSTRAINT `accelerator_entrepreneurpro_entrepreneurprofile_id_eed237ef_uniq` UNIQUE (`entrepreneurprofile_id`, `interestcategory_id`);
ALTER TABLE `accelerator_entrepreneurprofile_program_families` ADD CONSTRAINT `b116f475a0c260a87e012292bc9eea92` FOREIGN KEY (`entrepreneurprofile_id`) REFERENCES `accelerator_entrepreneurprofile` (`id`);
ALTER TABLE `accelerator_entrepreneurprofile_program_families` ADD CONSTRAINT `accele_programfamily_id_fee3c6bd_fk_accelerator_programfamily_id` FOREIGN KEY (`programfamily_id`) REFERENCES `accelerator_programfamily` (`id`);
ALTER TABLE `accelerator_entrepreneurprofile_program_families` ADD CONSTRAINT `accelerator_entrepreneurpro_entrepreneurprofile_id_243c9826_uniq` UNIQUE (`entrepreneurprofile_id`, `programfamily_id`);
ALTER TABLE `accelerator_entrepreneurprofile_recommendation_tags` ADD CONSTRAINT `d5ee3e11824e49cfd87fa37e5ff7c361` FOREIGN KEY (`entrepreneurprofile_id`) REFERENCES `accelerator_entrepreneurprofile` (`id`);
ALTER TABLE `accelerator_entrepreneurprofile_recommendation_tags` ADD CONSTRAINT `D7af28cf1ae8688411d3b50eb46e35e8` FOREIGN KEY (`recommendationtag_id`) REFERENCES `accelerator_recommendationtag` (`id`);
ALTER TABLE `accelerator_entrepreneurprofile_recommendation_tags` ADD CONSTRAINT `accelerator_entrepreneurpro_entrepreneurprofile_id_9a0b6272_uniq` UNIQUE (`entrepreneurprofile_id`, `recommendationtag_id`);
ALTER TABLE `accelerator_entrepreneurprofile` ADD CONSTRAINT `accelerator_entrepreneurprofile_user_id_d6ea0f93_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `accelerator_bucketstate_fae0fb83` ON `accelerator_bucketstate` (`program_role_id`);
ALTER TABLE `accelerator_bucketstate` ADD CONSTRAINT `accelerat_program_role_id_da53e747_fk_accelerator_programrole_id` FOREIGN KEY (`program_role_id`) REFERENCES `accelerator_programrole` (`id`);
CREATE INDEX `accelerator_applicationpanelassignment_3be65887` ON `accelerator_applicationpanelassignment` (`panel_id`);
ALTER TABLE `accelerator_applicationpanelassignment` ADD CONSTRAINT `accelerator_applicatio_panel_id_1027242b_fk_accelerator_panel_id` FOREIGN KEY (`panel_id`) REFERENCES `accelerator_panel` (`id`);
CREATE INDEX `accelerator_applicationpanelassignment_adc0676c` ON `accelerator_applicationpanelassignment` (`scenario_id`);
ALTER TABLE `accelerator_applicationpanelassignment` ADD CONSTRAINT `accelerator_appl_scenario_id_af43c058_fk_accelerator_scenario_id` FOREIGN KEY (`scenario_id`) REFERENCES `accelerator_scenario` (`id`);
