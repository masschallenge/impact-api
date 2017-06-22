/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

create user masschallenge;
GRANT ALL PRIVILEGES ON *.* TO 'masschallenge'@'%' WITH GRANT OPTION;

/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_a7792de1` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=325 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=460 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=37893 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f0ee9890` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7866 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19835 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contentitem_iframe_iframeitem` (
  `contentitem_ptr_id` int(11) NOT NULL,
  `src` varchar(200) NOT NULL,
  `width` varchar(10) NOT NULL,
  `height` varchar(10) NOT NULL,
  PRIMARY KEY (`contentitem_ptr_id`),
  CONSTRAINT `contentitem_ptr_id_refs_id_3da9a5919e0d17ca` FOREIGN KEY (`contentitem_ptr_id`) REFERENCES `fluent_contents_contentitem` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contentitem_text_textitem` (
  `contentitem_ptr_id` int(11) NOT NULL,
  `text` longtext NOT NULL,
  `text_final` longtext,
  PRIMARY KEY (`contentitem_ptr_id`),
  CONSTRAINT `contentitem_ptr_id_refs_id_5deaf6e9348b7b88` FOREIGN KEY (`contentitem_ptr_id`) REFERENCES `fluent_contents_contentitem` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_refs_id_c8665aa` (`user_id`),
  KEY `content_type_id_refs_id_288599e6` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=160 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fluent_contents_contentitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `polymorphic_ctype_id` int(11) DEFAULT NULL,
  `parent_type_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `placeholder_id` int(11) DEFAULT NULL,
  `sort_order` int(11) NOT NULL,
  `language_code` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fluent_contents_contentitem_97604479` (`polymorphic_ctype_id`),
  KEY `fluent_contents_contentitem_d649a7a0` (`parent_type_id`),
  KEY `fluent_contents_contentitem_c1ca2850` (`placeholder_id`),
  KEY `fluent_contents_contentitem_a6f2084` (`sort_order`),
  KEY `fluent_contents_contentitem_da473cdf` (`language_code`),
  CONSTRAINT `parent_type_id_refs_id_28a11b3de4d7baf5` FOREIGN KEY (`parent_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `placeholder_id_refs_id_6af7340af8375ce2` FOREIGN KEY (`placeholder_id`) REFERENCES `fluent_contents_placeholder` (`id`),
  CONSTRAINT `polymorphic_ctype_id_refs_id_28a11b3de4d7baf5` FOREIGN KEY (`polymorphic_ctype_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=311 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fluent_contents_placeholder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(50) NOT NULL,
  `role` varchar(1) NOT NULL,
  `parent_type_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fluent_contents_placeholde_parent_type_id_451c85966d08dedf_uniq` (`parent_type_id`,`parent_id`,`slot`),
  KEY `fluent_contents_placeholder_400badfd` (`slot`),
  KEY `fluent_contents_placeholder_d649a7a0` (`parent_type_id`),
  CONSTRAINT `parent_type_id_refs_id_8f69ed642a29cde` FOREIGN KEY (`parent_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=326 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fluent_pages_htmlpage_translation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_code` varchar(15) NOT NULL,
  `meta_keywords` varchar(255) DEFAULT NULL,
  `meta_description` varchar(255) DEFAULT NULL,
  `meta_title` varchar(255) DEFAULT NULL,
  `master_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fluent_pages_htmlpage_trans_language_code_4e6b1e728c766487_uniq` (`language_code`,`master_id`),
  KEY `fluent_pages_htmlpage_translation_da473cdf` (`language_code`),
  KEY `fluent_pages_htmlpage_translation_11a5708d` (`master_id`),
  CONSTRAINT `master_id_refs_id_10e5f581` FOREIGN KEY (`master_id`) REFERENCES `fluent_pages_urlnode` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fluent_pages_pagelayout` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(50) NOT NULL,
  `title` varchar(255) NOT NULL,
  `template_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fluent_pages_pagelayout_45544485` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fluent_pages_urlnode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `polymorphic_ctype_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `parent_site_id` int(11) NOT NULL,
  `status` varchar(1) NOT NULL,
  `publication_date` datetime DEFAULT NULL,
  `publication_end_date` datetime DEFAULT NULL,
  `in_navigation` tinyint(1) NOT NULL,
  `author_id` int(11) NOT NULL,
  `creation_date` datetime NOT NULL,
  `modification_date` datetime NOT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  `icon` varchar(32) DEFAULT NULL,
  `key` varchar(50) DEFAULT NULL,
  `in_sitemaps` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fluent_pages_urlnode_parent_site_id_3daddc0a38955c49_uniq` (`parent_site_id`,`key`),
  KEY `fluent_pages_urlnode_97604479` (`polymorphic_ctype_id`),
  KEY `fluent_pages_urlnode_63f17a16` (`parent_id`),
  KEY `fluent_pages_urlnode_4e3180c7` (`parent_site_id`),
  KEY `fluent_pages_urlnode_cc846901` (`author_id`),
  KEY `fluent_pages_urlnode_42b06ff6` (`lft`),
  KEY `fluent_pages_urlnode_91543e5a` (`rght`),
  KEY `fluent_pages_urlnode_efd07f28` (`tree_id`),
  KEY `fluent_pages_urlnode_2a8f42e8` (`level`),
  KEY `fluent_pages_urlnode_c9ad71dd` (`status`),
  KEY `fluent_pages_urlnode_a221fe64` (`publication_end_date`),
  KEY `fluent_pages_urlnode_ee664462` (`publication_date`),
  KEY `fluent_pages_urlnode_3c0ea264` (`in_navigation`),
  KEY `fluent_pages_urlnode_c0d4be93` (`key`),
  KEY `fluent_pages_urlnode_8ca57ceb` (`in_sitemaps`),
  CONSTRAINT `author_id_refs_id_4290198e4f24741d` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `parent_id_refs_id_71ec6a1e02cc2613` FOREIGN KEY (`parent_id`) REFERENCES `fluent_pages_urlnode` (`id`),
  CONSTRAINT `parent_site_id_refs_id_18381885c8d2f614` FOREIGN KEY (`parent_site_id`) REFERENCES `django_site` (`id`),
  CONSTRAINT `polymorphic_ctype_id_refs_id_62288bb59cf04b67` FOREIGN KEY (`polymorphic_ctype_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=572 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fluent_pages_urlnode_translation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `override_url` varchar(255) NOT NULL,
  `_cached_url` varchar(255) DEFAULT NULL,
  `language_code` varchar(15) NOT NULL,
  `master_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fluent_pages_urlnode_transla_language_code_d4eb25430e18f4b_uniq` (`language_code`,`master_id`),
  KEY `fluent_pages_urlnode_translation_f52cfca0` (`slug`),
  KEY `fluent_pages_urlnode_translation_a855fe49` (`_cached_url`),
  KEY `fluent_pages_urlnode_translation_da473cdf` (`language_code`),
  KEY `fluent_pages_urlnode_translation_c0bac2ae` (`master_id`),
  CONSTRAINT `master_id_refs_id_3f6fb934` FOREIGN KEY (`master_id`) REFERENCES `fluent_pages_urlnode` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=583 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `application_type_id` int(11) NOT NULL,
  `application_status` varchar(64) DEFAULT NULL,
  `submission_datetime` datetime DEFAULT NULL,
  `cycle_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_application_92fe01c8` (`startup_id`),
  KEY `mc_application_ca71274b` (`application_type_id`),
  KEY `mc_application_d7b272e0` (`cycle_id`),
  CONSTRAINT `application_type_id_refs_id_1ae6bcbb8b7a51f7` FOREIGN KEY (`application_type_id`) REFERENCES `mc_applicationtype` (`id`),
  CONSTRAINT `mc_application_cycle_id_342a9e243209c5ac_fk_mc_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `mc_programcycle` (`id`),
  CONSTRAINT `startup_id_refs_id_7fcfeb6274a2cf06` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10006 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_applicationanswer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_id` int(11) NOT NULL,
  `application_question_id` int(11) NOT NULL,
  `answer_text` varchar(2000) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_applicationanswer_398529ef` (`application_id`),
  KEY `mc_applicationanswer_14a50a7d` (`application_question_id`),
  CONSTRAINT `application_id_refs_id_411fee7c8714c26b` FOREIGN KEY (`application_id`) REFERENCES `mc_application` (`id`),
  CONSTRAINT `application_question_id_refs_id_a46a5e5cf89082b` FOREIGN KEY (`application_question_id`) REFERENCES `mc_applicationquestion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=276794 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_applicationpanelassignment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_id` int(11) NOT NULL,
  `panel_id` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `panel_slot_number` int(11) DEFAULT NULL,
  `notes` varchar(200) NOT NULL,
  `remote_pitch` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_applicationpanelassignm_application_id_77696d5c58b0d103_uniq` (`application_id`,`scenario_id`,`panel_id`),
  KEY `mc_applicationpanelassignment_398529ef` (`application_id`),
  KEY `mc_applicationpanelassignment_130efbb7` (`panel_id`),
  KEY `mc_applicationpanelassignment_3bb529ba` (`scenario_id`),
  CONSTRAINT `application_id_refs_id_5152b4fd16cbc6e7` FOREIGN KEY (`application_id`) REFERENCES `mc_application` (`id`),
  CONSTRAINT `panel_id_refs_id_6789f726de3f20a3` FOREIGN KEY (`panel_id`) REFERENCES `mc_panel` (`id`),
  CONSTRAINT `scenario_id_refs_id_3a06b9ce88a7ff48` FOREIGN KEY (`scenario_id`) REFERENCES `mc_scenario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=603381 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_applicationquestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_type_id` int(11) NOT NULL,
  `question_number` int(11) NOT NULL,
  `section_heading` varchar(40) NOT NULL,
  `question_text` varchar(200) NOT NULL,
  `help_text` varchar(1000) NOT NULL,
  `mandatory` tinyint(1) NOT NULL,
  `text_box_lines` int(11) NOT NULL,
  `text_limit` int(11) NOT NULL,
  `text_limit_units` varchar(64) NOT NULL,
  `question_id` int(11) DEFAULT NULL,
  `choice_layout` varchar(64) NOT NULL,
  `choice_options` varchar(4000) NOT NULL,
  `question_type` varchar(64) NOT NULL,
  `program_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_applicationquestion_ca71274b` (`application_type_id`),
  KEY `mc_applicationquestion_7aa0f6ee` (`question_id`),
  KEY `mc_applicationquestion_429b1823` (`program_id`),
  CONSTRAINT `application_type_id_refs_id_3bdb0225e3315b49` FOREIGN KEY (`application_type_id`) REFERENCES `mc_applicationtype` (`id`),
  CONSTRAINT `mc_applicationquest_program_id_66498e7f19a549c0_fk_mc_program_id` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `mc_applicationque_question_id_7ef50c4fd6d26ced_fk_mc_question_id` FOREIGN KEY (`question_id`) REFERENCES `mc_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=625 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_applicationtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(500) NOT NULL,
  `submission_label_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_applicationtype_fcd6cf16` (`submission_label_id`),
  CONSTRAINT `mc_ap_submission_label_id_2abe624624af233c_fk_mc_startuplabel_id` FOREIGN KEY (`submission_label_id`) REFERENCES `mc_startuplabel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_baseprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_type` varchar(16) NOT NULL,
  `privacy_policy_accepted` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_1d847b571bf4a42f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37513 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=198 DEFAULT CHARSET=latin1;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `abbr` varchar(3) NOT NULL,
  `usd_exchange` double NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `abbr` (`abbr`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_entrepreneurprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `linked_in_url` varchar(200) NOT NULL,
  `facebook_url` varchar(200) NOT NULL,
  `twitter_handle` varchar(16) NOT NULL,
  `personal_website_url` varchar(255) NOT NULL,
  `image` varchar(100) NOT NULL,
  `drupal_id` int(11) DEFAULT NULL,
  `drupal_creation_date` datetime DEFAULT NULL,
  `drupal_last_login` datetime DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `users_last_activity` datetime DEFAULT NULL,
  `current_program_id` int(11) DEFAULT NULL,
  `current_page` varchar(200) NOT NULL,
  `bio` longtext NOT NULL,
  `landing_page` varchar(200) NOT NULL,
  `privacy_policy_accepted` tinyint(1) NOT NULL,
  `newsletter_sender` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `mc_entrepreneurprofile_3ff4c9e5` (`current_program_id`),
  CONSTRAINT `current_program_id_refs_id_2803c3595327da1f` FOREIGN KEY (`current_program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `user_id_refs_id_53baf31ff845a553` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29461 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_entrepreneurprofile_interest_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entrepreneurprofile_id` int(11) NOT NULL,
  `interestcategory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_entrepreneurpro_entrepreneurprofile_id_4523906403fd95f0_uniq` (`entrepreneurprofile_id`,`interestcategory_id`),
  KEY `mc_entrepreneurprofile_interest_categories_35e701e5` (`entrepreneurprofile_id`),
  KEY `mc_entrepreneurprofile_interest_categories_3ba61f0a` (`interestcategory_id`),
  CONSTRAINT `a07f6664492cc0cba93055647e445144` FOREIGN KEY (`entrepreneurprofile_id`) REFERENCES `mc_entrepreneurprofile` (`id`),
  CONSTRAINT `m_interestcategory_id_2f9bce490cc7e7d1_fk_mc_interestcategory_id` FOREIGN KEY (`interestcategory_id`) REFERENCES `mc_interestcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33065 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_entrepreneurprofile_program_families` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entrepreneurprofile_id` int(11) NOT NULL,
  `programfamily_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_entrepreneurpro_entrepreneurprofile_id_45dde2434621f03a_uniq` (`entrepreneurprofile_id`,`programfamily_id`),
  KEY `mc_entrepreneurprofile_program_families_35e701e5` (`entrepreneurprofile_id`),
  KEY `mc_entrepreneurprofile_program_families_d2344029` (`programfamily_id`),
  CONSTRAINT `D9f96e023f330f1daf1afb9f5777eb27` FOREIGN KEY (`entrepreneurprofile_id`) REFERENCES `mc_entrepreneurprofile` (`id`),
  CONSTRAINT `mc_entr_programfamily_id_77da24e7f7fe1da3_fk_mc_programfamily_id` FOREIGN KEY (`programfamily_id`) REFERENCES `mc_programfamily` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45778 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_entrepreneurprofile_recommendation_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entrepreneurprofile_id` int(11) NOT NULL,
  `recommendationtag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_entrepreneurpro_entrepreneurprofile_id_322df36b16f6ec54_uniq` (`entrepreneurprofile_id`,`recommendationtag_id`),
  KEY `mc_entrepreneurprofile_recommendation_tags_35e701e5` (`entrepreneurprofile_id`),
  KEY `mc_entrepreneurprofile_recommendation_tags_d1dd995a` (`recommendationtag_id`),
  CONSTRAINT `b5810e72efd01d2bff8625c14ee09bbb` FOREIGN KEY (`recommendationtag_id`) REFERENCES `mc_recommendationtag` (`id`),
  CONSTRAINT `D5013c86b0f9f94ffad092bd1b672724` FOREIGN KEY (`entrepreneurprofile_id`) REFERENCES `mc_entrepreneurprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=431100 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expert_related_industry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expertprofile_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_expert_related_indust_expertprofile_id_19181e4364289430_uniq` (`expertprofile_id`,`industry_id`),
  KEY `mc_expert_related_industry_ab5ddbd6` (`expertprofile_id`),
  KEY `mc_expert_related_industry_d28c39ae` (`industry_id`),
  CONSTRAINT `expertprofile_id_refs_id_14cae85379b9b8c5` FOREIGN KEY (`expertprofile_id`) REFERENCES `mc_expertprofile` (`id`),
  CONSTRAINT `industry_id_refs_id_3b708537687d787d` FOREIGN KEY (`industry_id`) REFERENCES `mc_industry` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56803 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expert_related_mentoringspecialty` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expertprofile_id` int(11) NOT NULL,
  `mentoringspecialties_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_expert_related_mentor_expertprofile_id_53f3c886bc5e586e_uniq` (`expertprofile_id`,`mentoringspecialties_id`),
  KEY `mc_expert_related_mentoringspecialty_ab5ddbd6` (`expertprofile_id`),
  KEY `mc_expert_related_mentoringspecialty_c8f3748f` (`mentoringspecialties_id`),
  CONSTRAINT `expertprofile_id_refs_id_3f465ca18c84b72c` FOREIGN KEY (`expertprofile_id`) REFERENCES `mc_expertprofile` (`id`),
  CONSTRAINT `mentoringspecialties_id_refs_id_3f8513d1ac2a54bd` FOREIGN KEY (`mentoringspecialties_id`) REFERENCES `mc_mentoringspecialties` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25367 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expertcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expertinterest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `program_family_id` int(11) NOT NULL,
  `interest_type_id` int(11) NOT NULL,
  `topics` longtext NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_expertinterest_fbfc09f1` (`user_id`),
  KEY `mc_expertinterest_8d00c2c3` (`program_family_id`),
  KEY `mc_expertinterest_4322a5c8` (`interest_type_id`),
  CONSTRAINT `interest_type_id_refs_id_5e5522cc50fd83bf` FOREIGN KEY (`interest_type_id`) REFERENCES `mc_expertinteresttype` (`id`),
  CONSTRAINT `program_family_id_refs_id_1f6adf119f933ad4` FOREIGN KEY (`program_family_id`) REFERENCES `mc_programfamily` (`id`),
  CONSTRAINT `user_id_refs_id_7d07b2a174293620` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3514 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expertinteresttype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `short_description` varchar(255) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expertprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `linked_in_url` varchar(200) NOT NULL,
  `facebook_url` varchar(200) NOT NULL,
  `twitter_handle` varchar(16) NOT NULL,
  `personal_website_url` varchar(255) NOT NULL,
  `salutation` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL,
  `bio` longtext NOT NULL,
  `expert_category_id` int(11) NOT NULL,
  `primary_industry_expertise_id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `privacy_email` varchar(64) NOT NULL,
  `privacy_phone` varchar(64) NOT NULL,
  `privacy_web` varchar(64) NOT NULL,
  `judge_interest` tinyint(1) NOT NULL,
  `mentor_interest` tinyint(1) NOT NULL,
  `speaker_interest` tinyint(1) NOT NULL,
  `speaker_topics` longtext NOT NULL,
  `office_hours_interest` tinyint(1) NOT NULL,
  `office_hours_topics` longtext NOT NULL,
  `drupal_id` int(11) DEFAULT NULL,
  `drupal_creation_date` datetime DEFAULT NULL,
  `drupal_last_login` datetime DEFAULT NULL,
  `expert_group` varchar(10) NOT NULL,
  `reliability` decimal(3,2) DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `referred_by` longtext NOT NULL,
  `other_potential_experts` longtext NOT NULL,
  `internal_notes` longtext NOT NULL,
  `users_last_activity` datetime DEFAULT NULL,
  `current_program_id` int(11) DEFAULT NULL,
  `current_page` varchar(200) NOT NULL,
  `landing_page` varchar(200) NOT NULL,
  `privacy_policy_accepted` tinyint(1) NOT NULL,
  `home_program_family_id` int(11) NOT NULL,
  `public_website_consent` tinyint(1) NOT NULL,
  `public_website_consent_checked` tinyint(1) NOT NULL,
  `newsletter_sender` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `mc_expertprofile_13b5d1c8` (`expert_category_id`),
  KEY `mc_expertprofile_1d397c99` (`primary_industry_expertise_id`),
  KEY `mc_expertprofile_3ff4c9e5` (`current_program_id`),
  KEY `mc_expertprofile_9459abc0` (`home_program_family_id`),
  CONSTRAINT `current_program_id_refs_id_422bf68180f07688` FOREIGN KEY (`current_program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `expert_category_id_refs_id_5e81f405336eabf7` FOREIGN KEY (`expert_category_id`) REFERENCES `mc_expertcategory` (`id`),
  CONSTRAINT `m_home_program_family_id_7195f1d6c310c128_fk_mc_programfamily_id` FOREIGN KEY (`home_program_family_id`) REFERENCES `mc_programfamily` (`id`),
  CONSTRAINT `primary_industry_expertise_id_refs_id_30c7ef4ca2f4832f` FOREIGN KEY (`primary_industry_expertise_id`) REFERENCES `mc_industry` (`id`),
  CONSTRAINT `user_id_refs_id_40501eb44c4c9fa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5599 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expertprofile_functional_expertise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expertprofile_id` int(11) NOT NULL,
  `functionalexpertise_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_expertprofile_function_expertprofile_id_6c541566600e150_uniq` (`expertprofile_id`,`functionalexpertise_id`),
  KEY `mc_expertprofile_functional_expertise_ab5ddbd6` (`expertprofile_id`),
  KEY `mc_expertprofile_functional_expertise_661e48e7` (`functionalexpertise_id`),
  CONSTRAINT `D0b7eb046846dfad308c321671208e09` FOREIGN KEY (`functionalexpertise_id`) REFERENCES `mc_functionalexpertise` (`id`),
  CONSTRAINT `mc_exper_expertprofile_id_422537af22076b9_fk_mc_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `mc_expertprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=299101 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expertprofile_interest_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expertprofile_id` int(11) NOT NULL,
  `interestcategory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_expertprofile_interes_expertprofile_id_764150abf55a75c0_uniq` (`expertprofile_id`,`interestcategory_id`),
  KEY `mc_expertprofile_interest_categories_ab5ddbd6` (`expertprofile_id`),
  KEY `mc_expertprofile_interest_categories_3ba61f0a` (`interestcategory_id`),
  CONSTRAINT `mc_exper_expertprofile_id_7e00099e73a0332_fk_mc_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `mc_expertprofile` (`id`),
  CONSTRAINT `m_interestcategory_id_6ef95b1ffae507ce_fk_mc_interestcategory_id` FOREIGN KEY (`interestcategory_id`) REFERENCES `mc_interestcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2588 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expertprofile_program_families` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expertprofile_id` int(11) NOT NULL,
  `programfamily_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_expertprofile_program_expertprofile_id_6f3222a509a35d42_uniq` (`expertprofile_id`,`programfamily_id`),
  KEY `mc_expertprofile_program_families_ab5ddbd6` (`expertprofile_id`),
  KEY `mc_expertprofile_program_families_d2344029` (`programfamily_id`),
  CONSTRAINT `mc_exper_expertprofile_id_196e5da0e05f867_fk_mc_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `mc_expertprofile` (`id`),
  CONSTRAINT `mc_expe_programfamily_id_6fc0dc82fe2259c8_fk_mc_programfamily_id` FOREIGN KEY (`programfamily_id`) REFERENCES `mc_programfamily` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20185 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_expertprofile_recommendation_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expertprofile_id` int(11) NOT NULL,
  `recommendationtag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_expertprofile_recomme_expertprofile_id_3df8d461fa233b3a_uniq` (`expertprofile_id`,`recommendationtag_id`),
  KEY `mc_expertprofile_recommendation_tags_ab5ddbd6` (`expertprofile_id`),
  KEY `mc_expertprofile_recommendation_tags_d1dd995a` (`recommendationtag_id`),
  CONSTRAINT `D84638728bd07d6132d58b970de36bb8` FOREIGN KEY (`recommendationtag_id`) REFERENCES `mc_recommendationtag` (`id`),
  CONSTRAINT `mc_expe_expertprofile_id_592fae483003d2c8_fk_mc_expertprofile_id` FOREIGN KEY (`expertprofile_id`) REFERENCES `mc_expertprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=271996 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_functionalexpertise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mc_functionalexpertise_63f17a16` (`parent_id`),
  KEY `mc_functionalexpertise_42b06ff6` (`lft`),
  KEY `mc_functionalexpertise_91543e5a` (`rght`),
  KEY `mc_functionalexpertise_efd07f28` (`tree_id`),
  KEY `mc_functionalexpertise_2a8f42e8` (`level`),
  CONSTRAINT `parent_id_refs_id_868974a5` FOREIGN KEY (`parent_id`) REFERENCES `mc_functionalexpertise` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=185 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_industry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  `icon` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mc_industry_63f17a16` (`parent_id`),
  KEY `mc_industry_42b06ff6` (`lft`),
  KEY `mc_industry_91543e5a` (`rght`),
  KEY `mc_industry_efd07f28` (`tree_id`),
  KEY `mc_industry_2a8f42e8` (`level`),
  CONSTRAINT `parent_id_refs_id_6ed29eaa37008679` FOREIGN KEY (`parent_id`) REFERENCES `mc_industry` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_interestcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(127) NOT NULL,
  `description` varchar(500) NOT NULL,
  `program_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_interestcategory_7eef53e3` (`program_id`),
  CONSTRAINT `program_id_refs_id_15d5dfa7cd996b28` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_jobposting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `postdate` datetime NOT NULL,
  `type` varchar(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `applicationemail` varchar(100) DEFAULT NULL,
  `more_info_url` varchar(100) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_jobposting_92fe01c8` (`startup_id`),
  CONSTRAINT `startup_id_refs_id_1f83d97ae8b1396c` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=284 DEFAULT CHARSET=utf8;

SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `mc_judge_assignment_counts_v` (
  `judge_id` tinyint NOT NULL,
  `first_name` tinyint NOT NULL,
  `last_name` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `round_name` tinyint NOT NULL,
  `total_assigned` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `mc_judge_commitments_r1reg_v` (
  `User ID` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `first_name` tinyint NOT NULL,
  `last_name` tinyint NOT NULL,
  `capacity` tinyint NOT NULL,
  `Program Name` tinyint NOT NULL,
  `Round_Name` tinyint NOT NULL,
  `Commitment ID` tinyint NOT NULL,
  `Round ID` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `mc_judge_commitments_v` (
  `User ID` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `first_name` tinyint NOT NULL,
  `last_name` tinyint NOT NULL,
  `capacity` tinyint NOT NULL,
  `Program Name` tinyint NOT NULL,
  `Round_Name` tinyint NOT NULL,
  `Commitment ID` tinyint NOT NULL,
  `Round ID` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `mc_judge_completed_feedback_counts_v` (
  `judge_id` tinyint NOT NULL,
  `first_name` tinyint NOT NULL,
  `last_name` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `round_name` tinyint NOT NULL,
  `completed_feedbacks` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `mc_judge_progress_v` (
  `id` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `judge_id` tinyint NOT NULL,
  `first_name` tinyint NOT NULL,
  `last_name` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `capacity` tinyint NOT NULL,
  `Total Assigned` tinyint NOT NULL,
  `Total Completed` tinyint NOT NULL,
  `Total Uncompleted` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgeapplicationfeedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_id` int(11) NOT NULL,
  `form_type_id` int(11) NOT NULL,
  `judge_id` int(11) NOT NULL,
  `panel_id` int(11) NOT NULL,
  `judging_status` int(11) DEFAULT NULL,
  `feedback_status` varchar(20) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_judgeapplicationfeedback_judge_id_70ef10bbe77ffc82_uniq` (`judge_id`,`application_id`,`panel_id`),
  KEY `mc_judgeapplicationfeedback_398529ef` (`application_id`),
  KEY `mc_judgeapplicationfeedback_a2e1b040` (`form_type_id`),
  KEY `mc_judgeapplicationfeedback_bcb024b0` (`judge_id`),
  KEY `mc_judgeapplicationfeedback_130efbb7` (`panel_id`),
  CONSTRAINT `application_id_refs_id_7e82e59f3ba4b370` FOREIGN KEY (`application_id`) REFERENCES `mc_application` (`id`),
  CONSTRAINT `form_type_id_refs_id_7492120ae35e1848` FOREIGN KEY (`form_type_id`) REFERENCES `mc_judgingform` (`id`),
  CONSTRAINT `judge_id_refs_id_21504b8905ba9b3c` FOREIGN KEY (`judge_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `panel_id_refs_id_56a7c73b7764919a` FOREIGN KEY (`panel_id`) REFERENCES `mc_panel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66067 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgeavailability` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `commitment_id` int(11) NOT NULL,
  `panel_location_id` varchar(225) DEFAULT NULL,
  `panel_time_id` int(11) DEFAULT NULL,
  `panel_type_id` varchar(225) DEFAULT NULL,
  `availability_type` varchar(32) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_judgeavailability_commitment_id_38b962faff131c43_uniq` (`commitment_id`,`panel_location_id`,`panel_time_id`,`panel_type_id`),
  KEY `mc_judgeavailability_6a6b8869` (`commitment_id`),
  KEY `mc_judgeavailability_abc2343a` (`panel_location_id`),
  KEY `mc_judgeavailability_efe7ff4c` (`panel_time_id`),
  KEY `mc_judgeavailability_44f22665` (`panel_type_id`),
  CONSTRAINT `commitment_id_refs_id_44f254f6c704321e` FOREIGN KEY (`commitment_id`) REFERENCES `mc_judgeroundcommitment` (`id`),
  CONSTRAINT `mc_judgeavailability_panel_location_id_3385fbae70f70c9d_fk` FOREIGN KEY (`panel_location_id`) REFERENCES `mc_panellocation` (`location`),
  CONSTRAINT `mc_judgeavailability_panel_type_id_22a3b26b20eeb6e8_fk` FOREIGN KEY (`panel_type_id`) REFERENCES `mc_paneltype` (`panel_type`),
  CONSTRAINT `panel_time_id_refs_id_1f100ed1682f2ec6` FOREIGN KEY (`panel_time_id`) REFERENCES `mc_paneltime` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6345 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgefeedbackcomponent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback_element_id` int(11) NOT NULL,
  `answer_text` varchar(2000) NOT NULL,
  `judge_feedback_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_judgefeedbackcompo_feedback_element_id_4d3bc9f4668678fe_uniq` (`feedback_element_id`,`judge_feedback_id`),
  KEY `mc_judgefeedbackcomponent_206f544c` (`feedback_element_id`),
  KEY `mc_judgefeedbackcomponent_5691d10d` (`judge_feedback_id`),
  CONSTRAINT `feedback_element_id_refs_id_54d63a9dd219c340` FOREIGN KEY (`feedback_element_id`) REFERENCES `mc_judgingformelement` (`id`),
  CONSTRAINT `judge_feedback_id_refs_id_4b0ec21190418310` FOREIGN KEY (`judge_feedback_id`) REFERENCES `mc_judgeapplicationfeedback` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=656871 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgepanelassignment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judge_id` int(11) NOT NULL,
  `panel_id` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `assignment_status` varchar(16) NOT NULL,
  `panel_sequence_number` int(10) unsigned DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_judgepanelassignment_judge_id_30b854c0fc612ceb_uniq` (`judge_id`,`scenario_id`,`panel_id`),
  KEY `mc_judgepanelassignment_bcb024b0` (`judge_id`),
  KEY `mc_judgepanelassignment_130efbb7` (`panel_id`),
  KEY `mc_judgepanelassignment_3bb529ba` (`scenario_id`),
  CONSTRAINT `judge_id_refs_id_2e53b26d8b2e6346` FOREIGN KEY (`judge_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `panel_id_refs_id_1a1d9102228bb270` FOREIGN KEY (`panel_id`) REFERENCES `mc_panel` (`id`),
  CONSTRAINT `scenario_id_refs_id_3e0e5c1c02b44c5b` FOREIGN KEY (`scenario_id`) REFERENCES `mc_scenario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70134 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgeroundcommitment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judge_id` int(11) NOT NULL,
  `judging_round_id` int(11) NOT NULL,
  `capacity` int(11) DEFAULT NULL,
  `current_quota` int(11) DEFAULT NULL,
  `commitment_state` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_judgeroundcommitment_judge_id_3d1fe8bc1847797a_uniq` (`judge_id`,`judging_round_id`),
  KEY `mc_judgeroundcommitment_bcb024b0` (`judge_id`),
  KEY `mc_judgeroundcommitment_7164203c` (`judging_round_id`),
  CONSTRAINT `judge_id_refs_id_23f940ec2b2eef0` FOREIGN KEY (`judge_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `judging_round_id_refs_id_2e1cd73270a75621` FOREIGN KEY (`judging_round_id`) REFERENCES `mc_judginground` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7791 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgeroundcommitment_snapshot_apr13` (
  `id` int(11) NOT NULL DEFAULT '0',
  `judge_id` int(11) NOT NULL,
  `judging_round_id` int(11) NOT NULL,
  `capacity` int(11) DEFAULT NULL,
  `current_quota` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgeroundcommitment_snapshot_apr6` (
  `id` int(11) NOT NULL DEFAULT '0',
  `judge_id` int(11) NOT NULL,
  `judging_round_id` int(11) NOT NULL,
  `capacity` int(11) DEFAULT NULL,
  `current_quota` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgingform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(500) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgingformelement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `form_type_id` int(11) NOT NULL,
  `element_number` int(11) NOT NULL,
  `section_heading` varchar(40) NOT NULL,
  `question_text` varchar(200) NOT NULL,
  `help_text` varchar(1000) NOT NULL,
  `element_type` varchar(64) NOT NULL,
  `mandatory` tinyint(1) NOT NULL,
  `text_box_lines` int(11) DEFAULT NULL,
  `text_limit` int(11) DEFAULT NULL,
  `text_limit_units` varchar(64) NOT NULL,
  `choice_options` varchar(200) NOT NULL,
  `choice_layout` varchar(64) NOT NULL,
  `application_question_id` int(11) DEFAULT NULL,
  `feedback_type` varchar(64) NOT NULL,
  `element_name` varchar(50) NOT NULL,
  `display_value` varchar(64) NOT NULL,
  `text_minimum` int(11) DEFAULT NULL,
  `text_minimum_units` varchar(64) NOT NULL,
  `dashboard_label` varchar(50) NOT NULL,
  `sharing` varchar(64) NOT NULL,
  `score_element` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_judgingformelement_a2e1b040` (`form_type_id`),
  KEY `mc_judgingformelement_14a50a7d` (`application_question_id`),
  CONSTRAINT `application_question_id_refs_id_1e8585dee6892060` FOREIGN KEY (`application_question_id`) REFERENCES `mc_applicationquestion` (`id`),
  CONSTRAINT `form_type_id_refs_id_382ba371eeb4018` FOREIGN KEY (`form_type_id`) REFERENCES `mc_judgingform` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=993 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judginground` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  `start_date_time` datetime DEFAULT NULL,
  `end_date_time` datetime DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `round_type` varchar(10) NOT NULL,
  `application_type_id` int(11) DEFAULT NULL,
  `judging_form_id` int(11) DEFAULT NULL,
  `recruit_judges` varchar(16) NOT NULL,
  `recruiting_prompt` longtext NOT NULL,
  `capture_capacity` tinyint(1) NOT NULL,
  `capacity_prompt` longtext NOT NULL,
  `capacity_options` varchar(255) NOT NULL,
  `feedback_display` varchar(10) NOT NULL,
  `feedback_display_message` longtext NOT NULL,
  `feedback_display_items` varchar(64) NOT NULL,
  `feedback_merge_with_id` int(11) DEFAULT NULL,
  `capture_availability` varchar(32) NOT NULL,
  `negative_recruiting_prompt` longtext NOT NULL,
  `positive_recruiting_prompt` longtext NOT NULL,
  `judge_instructions` longtext NOT NULL,
  `presentation_mins` int(11) NOT NULL,
  `buffer_mins` int(11) NOT NULL,
  `break_mins` int(11) NOT NULL,
  `num_breaks` int(11) NOT NULL,
  `desired_judge_label_id` int(11) DEFAULT NULL,
  `startup_label_id` int(11) DEFAULT NULL,
  `confirmed_judge_label_id` int(11) DEFAULT NULL,
  `buffer_before_event` int(11) NOT NULL,
  `cycle_based_round` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_judginground_program_id_670d689f64eaff1d_uniq` (`program_id`,`name`),
  KEY `mc_judginground_7eef53e3` (`program_id`),
  KEY `mc_judginground_ca71274b` (`application_type_id`),
  KEY `mc_judginground_beebb9e3` (`judging_form_id`),
  KEY `mc_judginground_be093638` (`feedback_merge_with_id`),
  KEY `mc_judginground_413c41b4` (`desired_judge_label_id`),
  KEY `mc_judginground_5926436d` (`startup_label_id`),
  KEY `mc_judginground_bdf8c73e` (`confirmed_judge_label_id`),
  CONSTRAINT `application_type_id_refs_id_6f47be07ec7b84ec` FOREIGN KEY (`application_type_id`) REFERENCES `mc_applicationtype` (`id`),
  CONSTRAINT `feedback_merge_with_id_refs_id_12c10efcc1a2280b` FOREIGN KEY (`feedback_merge_with_id`) REFERENCES `mc_judginground` (`id`),
  CONSTRAINT `judging_form_id_refs_id_4e632bc157e0b3e0` FOREIGN KEY (`judging_form_id`) REFERENCES `mc_judgingform` (`id`),
  CONSTRAINT `mc_judgi_startup_label_id_12646c8cbb818997_fk_mc_startuplabel_id` FOREIGN KEY (`startup_label_id`) REFERENCES `mc_startuplabel` (`id`),
  CONSTRAINT `mc_ju_desired_judge_label_id_3abf6794e8853ae4_fk_mc_userlabel_id` FOREIGN KEY (`desired_judge_label_id`) REFERENCES `mc_userlabel` (`id`),
  CONSTRAINT `mc__confirmed_judge_label_id_46054c189748a62b_fk_mc_userlabel_id` FOREIGN KEY (`confirmed_judge_label_id`) REFERENCES `mc_userlabel` (`id`),
  CONSTRAINT `program_id_refs_id_4472e0aeb0ea1b8a` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_judgingroundstage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judging_round_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `start_date_time` datetime NOT NULL,
  `end_date_time` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_judgingroundstage_judging_round_id_11d346a965cf727_uniq` (`judging_round_id`,`name`),
  KEY `mc_judgingroundstage_7164203c` (`judging_round_id`),
  CONSTRAINT `judging_round_id_refs_id_3aea9d09fd2e5390` FOREIGN KEY (`judging_round_id`) REFERENCES `mc_judginground` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_memberprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `linked_in_url` varchar(200) NOT NULL,
  `facebook_url` varchar(200) NOT NULL,
  `twitter_handle` varchar(16) NOT NULL,
  `personal_website_url` varchar(255) NOT NULL,
  `image` varchar(100) NOT NULL,
  `drupal_id` int(11) DEFAULT NULL,
  `drupal_creation_date` datetime DEFAULT NULL,
  `drupal_last_login` datetime DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `users_last_activity` datetime DEFAULT NULL,
  `current_program_id` int(11) DEFAULT NULL,
  `current_page` varchar(200) NOT NULL,
  `landing_page` varchar(200) NOT NULL,
  `privacy_policy_accepted` tinyint(1) NOT NULL,
  `newsletter_sender` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `mc_memberprofile_3ff4c9e5` (`current_program_id`),
  CONSTRAINT `current_program_id_refs_id_272f151a5dd5d322` FOREIGN KEY (`current_program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `user_id_refs_id_66d8d111695cf610` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2816 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_memberprofile_interest_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `memberprofile_id` int(11) NOT NULL,
  `interestcategory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_memberprofile_interes_memberprofile_id_42ef6b43fb37b0dc_uniq` (`memberprofile_id`,`interestcategory_id`),
  KEY `mc_memberprofile_interest_categories_9b34fcb0` (`memberprofile_id`),
  KEY `mc_memberprofile_interest_categories_3ba61f0a` (`interestcategory_id`),
  CONSTRAINT `mc_memb_memberprofile_id_752cd90e9d0130a2_fk_mc_memberprofile_id` FOREIGN KEY (`memberprofile_id`) REFERENCES `mc_memberprofile` (`id`),
  CONSTRAINT `m_interestcategory_id_7422926df6db4628_fk_mc_interestcategory_id` FOREIGN KEY (`interestcategory_id`) REFERENCES `mc_interestcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_memberprofile_program_families` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `memberprofile_id` int(11) NOT NULL,
  `programfamily_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_memberprofile_program_memberprofile_id_2520e8078b5f622e_uniq` (`memberprofile_id`,`programfamily_id`),
  KEY `mc_memberprofile_program_families_9b34fcb0` (`memberprofile_id`),
  KEY `mc_memberprofile_program_families_d2344029` (`programfamily_id`),
  CONSTRAINT `mc_membe_memberprofile_id_929b254027cc1af_fk_mc_memberprofile_id` FOREIGN KEY (`memberprofile_id`) REFERENCES `mc_memberprofile` (`id`),
  CONSTRAINT `mc_memb_programfamily_id_6b0fe4f6a30c3fb6_fk_mc_programfamily_id` FOREIGN KEY (`programfamily_id`) REFERENCES `mc_programfamily` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1399 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_memberprofile_recommendation_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `memberprofile_id` int(11) NOT NULL,
  `recommendationtag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_memberprofile_recomme_memberprofile_id_4007ecf009453f3a_uniq` (`memberprofile_id`,`recommendationtag_id`),
  KEY `mc_memberprofile_recommendation_tags_9b34fcb0` (`memberprofile_id`),
  KEY `mc_memberprofile_recommendation_tags_d1dd995a` (`recommendationtag_id`),
  CONSTRAINT `ddf332b661ddab44950eb2cd13fd713c` FOREIGN KEY (`recommendationtag_id`) REFERENCES `mc_recommendationtag` (`id`),
  CONSTRAINT `mc_memb_memberprofile_id_19d20fb286cc9a4c_fk_mc_memberprofile_id` FOREIGN KEY (`memberprofile_id`) REFERENCES `mc_memberprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_mentoringspecialties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_mentorprogramofficehour` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `mentor_id` int(11) NOT NULL,
  `finalist_id` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `description` varchar(500) NOT NULL,
  `location` varchar(50) NOT NULL,
  `notify_reservation` tinyint(1) NOT NULL,
  `topics` varchar(500) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_mentorprogramofficehour_program_id_67770dd7afd85768_uniq` (`program_id`,`mentor_id`,`date`,`start_time`),
  KEY `mc_mentorprogramofficehour_7eef53e3` (`program_id`),
  KEY `mc_mentorprogramofficehour_cea652a7` (`mentor_id`),
  KEY `mc_mentorprogramofficehour_6f9cffd0` (`finalist_id`),
  KEY `mc_mentorprogramofficehour_effd9ef` (`start_time`),
  KEY `mc_mentorprogramofficehour_986cbc25` (`date`),
  KEY `mc_mentorprogramofficehour_801e862` (`end_time`),
  CONSTRAINT `finalist_id_refs_id_7a32d211b26580ec` FOREIGN KEY (`finalist_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `mentor_id_refs_id_7a32d211b26580ec` FOREIGN KEY (`mentor_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `program_id_refs_id_1209dc2deb18fe46` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13937 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_namedgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_newsletter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(127) NOT NULL,
  `subject` varchar(500) NOT NULL,
  `from_addr` varchar(255) DEFAULT NULL,
  `program_id` int(11) NOT NULL,
  `date_mailed` datetime DEFAULT NULL,
  `cc_addrs` varchar(500) DEFAULT NULL,
  `judging_round_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_newsletter_7eef53e3` (`program_id`),
  KEY `mc_newsletter_0cc25dbd` (`judging_round_id`),
  CONSTRAINT `mc_newsl_judging_round_id_184783f079f722e1_fk_mc_judginground_id` FOREIGN KEY (`judging_round_id`) REFERENCES `mc_judginground` (`id`),
  CONSTRAINT `program_id_refs_id_486be2905ede585` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=786 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_newsletter_recipient_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newsletter_id` int(11) NOT NULL,
  `programrole_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_newsletter_recipient_rol_newsletter_id_749b2e4648db18d9_uniq` (`newsletter_id`,`programrole_id`),
  KEY `mc_newsletter_recipient_roles_50580fc3` (`newsletter_id`),
  KEY `mc_newsletter_recipient_roles_f3d1817` (`programrole_id`),
  CONSTRAINT `mc_newsletter_newsletter_id_202e61d158de2eec_fk_mc_newsletter_id` FOREIGN KEY (`newsletter_id`) REFERENCES `mc_newsletter` (`id`),
  CONSTRAINT `mc_newslett_programrole_id_1d9b5be9d205b028_fk_mc_programrole_id` FOREIGN KEY (`programrole_id`) REFERENCES `mc_programrole` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3341 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_newsletterreceipt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newsletter_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_newlettersenttorecipient_50580fc3` (`newsletter_id`),
  KEY `mc_newlettersenttorecipient_fcd09624` (`recipient_id`),
  CONSTRAINT `newsletter_id_refs_id_69da804eb17d58f6` FOREIGN KEY (`newsletter_id`) REFERENCES `mc_newsletter` (`id`),
  CONSTRAINT `recipient_id_refs_id_6b6b3b7bdd7e6690` FOREIGN KEY (`recipient_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=173928 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_nodepublishedfor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_id` int(11) NOT NULL,
  `published_for_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_nodepublishedfor_474baebc` (`node_id`),
  KEY `mc_nodepublishedfor_300b475b` (`published_for_id`),
  CONSTRAINT `node_id_refs_id_7668734e349715a5` FOREIGN KEY (`node_id`) REFERENCES `fluent_pages_urlnode` (`id`),
  CONSTRAINT `published_for_id_refs_id_4921996d9d58f41` FOREIGN KEY (`published_for_id`) REFERENCES `mc_programrole` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=810 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_observer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `title` varchar(50) NOT NULL,
  `company` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `newsletter_sender` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=911 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_observer_newsletter_cc_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `observer_id` int(11) NOT NULL,
  `programrole_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `observer_id` (`observer_id`,`programrole_id`),
  KEY `mc_observer__programrole_id_9a41ac9ff4a847a_fk_mc_programrole_id` (`programrole_id`),
  CONSTRAINT `mc_observer_newsl_observer_id_1cd756e0597ffa2f_fk_mc_observer_id` FOREIGN KEY (`observer_id`) REFERENCES `mc_observer` (`id`),
  CONSTRAINT `mc_observer__programrole_id_9a41ac9ff4a847a_fk_mc_programrole_id` FOREIGN KEY (`programrole_id`) REFERENCES `mc_programrole` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_panel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `panel_time_id` int(11) DEFAULT NULL,
  `panel_type_id` varchar(225) DEFAULT NULL,
  `description` varchar(30) NOT NULL,
  `location_id` varchar(225) DEFAULT NULL,
  `status` varchar(30) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_panel_efe7ff4c` (`panel_time_id`),
  KEY `mc_panel_44f22665` (`panel_type_id`),
  KEY `mc_panel_319d859` (`location_id`),
  CONSTRAINT `mc_panel_location_id_380097c6504c912c_fk` FOREIGN KEY (`location_id`) REFERENCES `mc_panellocation` (`location`),
  CONSTRAINT `mc_panel_panel_type_id_766c2e5ff97a78d2_fk` FOREIGN KEY (`panel_type_id`) REFERENCES `mc_paneltype` (`panel_type`),
  CONSTRAINT `panel_time_id_refs_id_174f8daa48808dc` FOREIGN KEY (`panel_time_id`) REFERENCES `mc_paneltime` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55990 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_panel_sequence_updates` (
  `panel_id` int(11) DEFAULT NULL,
  `panel_sequence_number` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_panellocation` (
  `location` varchar(225) NOT NULL,
  `description` varchar(225) NOT NULL,
  `judging_round_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`location`),
  KEY `mc_panellocation_7164203c` (`judging_round_id`),
  CONSTRAINT `judging_round_id_refs_id_35a0f96a66e805d1` FOREIGN KEY (`judging_round_id`) REFERENCES `mc_judginground` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_paneltime` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day` varchar(255) NOT NULL,
  `time` varchar(255) NOT NULL,
  `start_date_time` datetime DEFAULT NULL,
  `end_date_time` datetime DEFAULT NULL,
  `judging_round_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_paneltime_7164203c` (`judging_round_id`),
  CONSTRAINT `judging_round_id_refs_id_fb3f1239d0c7143` FOREIGN KEY (`judging_round_id`) REFERENCES `mc_judginground` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=235 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_paneltype` (
  `panel_type` varchar(225) NOT NULL,
  `description` varchar(225) NOT NULL,
  `judging_round_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`panel_type`),
  KEY `mc_paneltype_7164203c` (`judging_round_id`),
  CONSTRAINT `judging_round_id_refs_id_51ed88ddea1bd320` FOREIGN KEY (`judging_round_id`) REFERENCES `mc_judginground` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_partner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `partner_logo` varchar(100) NOT NULL,
  `website_url` varchar(100) NOT NULL,
  `twitter_handle` varchar(40) NOT NULL,
  `public_inquiry_email` varchar(100) NOT NULL,
  `url_slug` varchar(64) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_partner_name_5f11b39aecd9374b_uniq` (`name`),
  UNIQUE KEY `mc_partner_url_slug_2c7587e0d9e00373_uniq` (`url_slug`)
) ENGINE=InnoDB AUTO_INCREMENT=3056 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_partnerteammember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `partner_id` int(11) NOT NULL,
  `team_member_id` int(11) NOT NULL,
  `partner_administrator` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_partnerteammember_partner_id_63570f79ede4df50_uniq` (`partner_id`,`team_member_id`),
  KEY `mc_partnerteammember_76043359` (`partner_id`),
  KEY `mc_partnerteammember_fb893391` (`team_member_id`),
  CONSTRAINT `partner_id_refs_id_3fc4e7d1f80d0752` FOREIGN KEY (`partner_id`) REFERENCES `mc_partner` (`id`),
  CONSTRAINT `team_member_id_refs_id_6c06035ae98cecae` FOREIGN KEY (`team_member_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4513 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_paypalpayment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(100) NOT NULL,
  `transaction` varchar(100) NOT NULL,
  `amount` decimal(7,2) NOT NULL,
  `startup_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `refundable` tinyint(1) NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `currency_code` varchar(3) NOT NULL,
  `cycle_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mc_paypalpayment_startup_id_a452d6a9c7377c6_fk_mc_startup_id` (`startup_id`),
  KEY `mc_paypalpayment_d7b272e0` (`cycle_id`),
  CONSTRAINT `mc_paypalpayment_cycle_id_9338e323147acdb_fk_mc_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `mc_programcycle` (`id`),
  CONSTRAINT `mc_paypalpayment_startup_id_a452d6a9c7377c6_fk_mc_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7240 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_paypalrefund` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(100) NOT NULL,
  `transaction` varchar(100) NOT NULL,
  `correlation` varchar(100) NOT NULL,
  `amount` decimal(7,2) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `payment_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mc_paypalrefund_376ebbba` (`payment_id`),
  CONSTRAINT `mc_paypalrefu_payment_id_14fdef3fc268286c_fk_mc_paypalpayment_id` FOREIGN KEY (`payment_id`) REFERENCES `mc_paypalpayment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=780 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_program` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(500) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `location` varchar(50) NOT NULL,
  `program_status` varchar(64) NOT NULL,
  `early_application_fee` decimal(7,2) NOT NULL,
  `regular_application_fee` decimal(7,2) NOT NULL,
  `interested_judge_message` longtext NOT NULL,
  `approved_judge_message` longtext NOT NULL,
  `interested_mentor_message` longtext NOT NULL,
  `approved_mentor_message` longtext NOT NULL,
  `interested_speaker_message` longtext NOT NULL,
  `approved_speaker_message` longtext NOT NULL,
  `interested_office_hours_message` longtext NOT NULL,
  `approved_office_hours_message` longtext NOT NULL,
  `refund_code_support` varchar(64) NOT NULL,
  `accepting_company_overviews` tinyint(1) NOT NULL,
  `many_codes_per_partner` tinyint(1) NOT NULL,
  `program_family_id` int(11) DEFAULT NULL,
  `currency_code` varchar(3) NOT NULL,
  `regular_fee_suffix` varchar(20) NOT NULL,
  `url_slug` varchar(30) NOT NULL,
  `cycle_id` int(11) DEFAULT NULL,
  `mentor_program_group_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_program_8d00c2c3` (`program_family_id`),
  KEY `mc_program_d7b272e0` (`cycle_id`),
  KEY `mc_program_6c161578` (`mentor_program_group_id`),
  CONSTRAINT `mc_program_cycle_id_61ff026c4e9874d6_fk_mc_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `mc_programcycle` (`id`),
  CONSTRAINT `mc__mentor_program_group_id_290821dbffcfb6ad_fk_mc_namedgroup_id` FOREIGN KEY (`mentor_program_group_id`) REFERENCES `mc_namedgroup` (`id`),
  CONSTRAINT `program_family_id_refs_id_7f820d719141b1dd` FOREIGN KEY (`program_family_id`) REFERENCES `mc_programfamily` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programadministrator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_programadministrator_user_id_42dafe96d7ff263c_uniq` (`user_id`),
  KEY `mc_programadministrator_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_20f44bb` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programadministrator_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `programadministrator_id` int(11) NOT NULL,
  `programadministratorpermission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_programadminis_programadministrator_id_4c358fa00d69e9cd_uniq` (`programadministrator_id`,`programadministratorpermission_id`),
  KEY `mc_programadministrator_permission_aed69401` (`programadministrator_id`),
  KEY `mc_programadministrator_permission_deef761c` (`programadministratorpermission_id`),
  CONSTRAINT `D18468f81b491e515a02ff217d9e0a75` FOREIGN KEY (`programadministratorpermission_id`) REFERENCES `mc_programadministratorpermission` (`id`),
  CONSTRAINT `D2cbd2c11193c4050251535700d82c74` FOREIGN KEY (`programadministrator_id`) REFERENCES `mc_programadministrator` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37798 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programadministratorpermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `model` varchar(64) NOT NULL,
  `permission` varchar(20) NOT NULL,
  `description` varchar(200) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_programadministratorpermission_7eef53e3` (`program_id`),
  CONSTRAINT `program_id_refs_id_4c261342fd890322` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3985 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programcycle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `applications_open` tinyint(1) NOT NULL,
  `application_open_date` datetime DEFAULT NULL,
  `application_early_deadline_date` datetime DEFAULT NULL,
  `application_final_deadline_date` datetime DEFAULT NULL,
  `accepting_references` tinyint(1) NOT NULL,
  `default_application_type_id` int(11) DEFAULT NULL,
  `default_overview_application_type_id` int(11) DEFAULT NULL,
  `hidden` tinyint(1) NOT NULL,
  `advertised_final_deadline` datetime DEFAULT NULL,
  `short_name` varchar(32) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `D2b532926918a76189b007bc07112d14` (`default_application_type_id`),
  KEY `D8fa969c4dd17aa719c0f7ef8e607772` (`default_overview_application_type_id`),
  CONSTRAINT `D2b532926918a76189b007bc07112d14` FOREIGN KEY (`default_application_type_id`) REFERENCES `mc_applicationtype` (`id`),
  CONSTRAINT `D8fa969c4dd17aa719c0f7ef8e607772` FOREIGN KEY (`default_overview_application_type_id`) REFERENCES `mc_applicationtype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programfamily` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `short_description` longtext NOT NULL,
  `url_slug` varchar(30) NOT NULL,
  `email_domain` varchar(30) NOT NULL,
  `phone_number` varchar(30) NOT NULL,
  `physical_address` longtext NOT NULL,
  `office_hour_bcc` varchar(100) DEFAULT NULL,
  `is_open` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programoverride` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `applications_open` tinyint(1) NOT NULL,
  `application_open_date` datetime DEFAULT NULL,
  `application_early_deadline_date` datetime DEFAULT NULL,
  `application_final_deadline_date` datetime DEFAULT NULL,
  `early_application_fee` decimal(7,2) NOT NULL,
  `regular_application_fee` decimal(7,2) NOT NULL,
  `cycle_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_programoverride_7eef53e3` (`program_id`),
  KEY `mc_programoverride_d7b272e0` (`cycle_id`),
  CONSTRAINT `mc_programoverri_cycle_id_7538130f79fdb192_fk_mc_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `mc_programcycle` (`id`),
  CONSTRAINT `program_id_refs_id_7570636eaeb2a465` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programpartner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `partner_id` int(11) NOT NULL,
  `partner_type_id` int(11) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_programpartner_7eef53e3` (`program_id`),
  KEY `mc_programpartner_76043359` (`partner_id`),
  KEY `mc_programpartner_89cc1785` (`partner_type_id`),
  CONSTRAINT `partner_id_refs_id_32013007824290dc` FOREIGN KEY (`partner_id`) REFERENCES `mc_partner` (`id`),
  CONSTRAINT `partner_type_id_refs_id_74ce1d0dcf90fb51` FOREIGN KEY (`partner_type_id`) REFERENCES `mc_programpartnertype` (`id`),
  CONSTRAINT `program_id_refs_id_54e90d1cf06e3d56` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6809 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programpartnertype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `partner_type` varchar(50) NOT NULL,
  `description` varchar(200) NOT NULL,
  `feature_in_footer` tinyint(1) NOT NULL,
  `sort_order` int(11) DEFAULT NULL,
  `badge_image` varchar(100) NOT NULL,
  `badge_display` varchar(30) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_programpartnertype_7eef53e3` (`program_id`),
  CONSTRAINT `program_id_refs_id_36f206d467928a92` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `user_role_id` int(11) DEFAULT NULL,
  `user_label_id` int(11) DEFAULT NULL,
  `landing_page` varchar(255) DEFAULT NULL,
  `newsletter_recipient` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `mc_programrole_7eef53e3` (`program_id`),
  KEY `mc_programrole_52094d6e` (`name`),
  KEY `mc_programrole_d4ca635b` (`user_role_id`),
  KEY `mc_programrole_75df8002` (`user_label_id`),
  CONSTRAINT `mc_programrole_user_label_id_69e5f79c4fc2c69f_fk_mc_userlabel_id` FOREIGN KEY (`user_label_id`) REFERENCES `mc_userlabel` (`id`),
  CONSTRAINT `program_id_refs_id_5589e8ca800fd225` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `user_role_id_refs_id_33207aed23234109` FOREIGN KEY (`user_role_id`) REFERENCES `mc_userrole` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=407 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programrolegrant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `program_role_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_programrolegrant_person_id_6ec78927b617036e_uniq` (`person_id`,`program_role_id`),
  KEY `mc_programrolegrant_21b911c5` (`person_id`),
  KEY `mc_programrolegrant_2f8d8f1d` (`program_role_id`),
  CONSTRAINT `person_id_refs_id_215c7e0829ed91da` FOREIGN KEY (`person_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `program_role_id_refs_id_138bb57401e5ad20` FOREIGN KEY (`program_role_id`) REFERENCES `mc_programrole` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=127874 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programstartupattribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `attribute_type` varchar(63) NOT NULL,
  `attribute_label` varchar(127) NOT NULL,
  `attribute_description` varchar(255) NOT NULL,
  `non_admin_viewable` tinyint(1) NOT NULL,
  `staff_viewable` tinyint(1) NOT NULL,
  `admin_viewable` tinyint(1) NOT NULL,
  `finalist_viewable` tinyint(1) NOT NULL,
  `mentor_viewable` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_programstartupattribute_program_id_112d0591fc7af0a_uniq` (`program_id`,`attribute_label`),
  KEY `mc_programstartupattribute_7eef53e3` (`program_id`),
  CONSTRAINT `program_id_refs_id_6f937825e2472b0` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_programstartupstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `startup_status` varchar(255) NOT NULL,
  `description` longtext,
  `startup_list_include` tinyint(1) NOT NULL,
  `startup_list_tab_title` varchar(50) DEFAULT NULL,
  `startup_list_tab_id` varchar(30) DEFAULT NULL,
  `startup_list_tab_order` int(11) DEFAULT NULL,
  `badge_image` varchar(100) NOT NULL,
  `badge_display` varchar(30) NOT NULL,
  `startup_list_tab_description` longtext NOT NULL,
  `include_stealth_startup_names` tinyint(1) NOT NULL,
  `status_group` varchar(50) DEFAULT NULL,
  `sort_order` int(11) DEFAULT NULL,
  `startup_role_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `startup_status` (`startup_status`),
  KEY `mc_programstartupstatus_7eef53e3` (`program_id`),
  KEY `mc_programstartupstatus_5f4af245` (`startup_role_id`),
  CONSTRAINT `mc_program_startup_role_id_18a0ee32b7188b0b_fk_mc_startuprole_id` FOREIGN KEY (`startup_role_id`) REFERENCES `mc_startuprole` (`id`),
  CONSTRAINT `program_id_refs_id_5d708c245f24e331` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=latin1;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `question_type` varchar(64) NOT NULL,
  `choice_options` varchar(4000) NOT NULL,
  `choice_layout` varchar(64) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_recommendationtag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91784 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_reference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `title` varchar(50) NOT NULL,
  `company` varchar(50) NOT NULL,
  `reference_hash` varchar(50) NOT NULL,
  `sent` datetime DEFAULT NULL,
  `accessed` datetime DEFAULT NULL,
  `submitted` datetime DEFAULT NULL,
  `confirmed_first_name` varchar(50) NOT NULL,
  `confirmed_last_name` varchar(50) NOT NULL,
  `confirmed_company` varchar(50) NOT NULL,
  `question_1_rating` int(11) DEFAULT NULL,
  `question_2_rating` int(11) DEFAULT NULL,
  `comments` longtext NOT NULL,
  `requesting_user_id` int(11) DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reference_hash` (`reference_hash`),
  KEY `mc_reference_398529ef` (`application_id`),
  KEY `mc_reference_f15d121c` (`requesting_user_id`),
  CONSTRAINT `application_id_refs_id_1cb6cebf80d5703a` FOREIGN KEY (`application_id`) REFERENCES `mc_application` (`id`),
  CONSTRAINT `mc_reference_requesting_user_id_5fda2b12709de33e_fk_auth_user_id` FOREIGN KEY (`requesting_user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7380 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_refundcode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unique_code` varchar(30) NOT NULL,
  `issued_to_id` int(11) DEFAULT NULL,
  `notes` varchar(300) NOT NULL,
  `maximum_uses` int(10) unsigned DEFAULT NULL,
  `discount` int(11) NOT NULL,
  `internal` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_code` (`unique_code`),
  KEY `mc_refundcode_1b81f678` (`issued_to_id`),
  CONSTRAINT `mc_refundcode_issued_to_id_5a6a15a5a3522b1_fk_mc_partner_id` FOREIGN KEY (`issued_to_id`) REFERENCES `mc_partner` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23062 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_refundcode_programs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `refundcode_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_refundcode_programs_refundcode_id_3f17a00435ed3b94_uniq` (`refundcode_id`,`program_id`),
  KEY `mc_refundcode_programs_88b5e867` (`refundcode_id`),
  KEY `mc_refundcode_programs_7eef53e3` (`program_id`),
  CONSTRAINT `mc_refundcode_progr_program_id_476a1ac1e58fc045_fk_mc_program_id` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `mc_refundcode_refundcode_id_1000b5d2e2207671_fk_mc_refundcode_id` FOREIGN KEY (`refundcode_id`) REFERENCES `mc_refundcode` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41274 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_refundcoderedemption` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `refund_code_id` int(11) NOT NULL,
  `redeemed_by_id` int(11) DEFAULT NULL,
  `refund_status` varchar(32) NOT NULL,
  `refund_transaction_id` varchar(500) NOT NULL,
  `refund_amount` decimal(7,2) NOT NULL,
  `startup_id` int(11) DEFAULT NULL,
  `cycle_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_refundcoderedemption_79446569` (`refund_code_id`),
  KEY `mc_refundcoderedemption_e151467a` (`redeemed_by_id`),
  KEY `mc_refundcoderedemption_99f77c8c` (`startup_id`),
  KEY `mc_refundcoderedemption_d7b272e0` (`cycle_id`),
  CONSTRAINT `mc_refundcoderedemp_startup_id_21b0be308b449a34_fk_mc_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`),
  CONSTRAINT `mc_refundcodered_cycle_id_3fce824be0457a6d_fk_mc_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `mc_programcycle` (`id`),
  CONSTRAINT `mc_refundco_redeemed_by_id_3739dad9f8401416_fk_mc_application_id` FOREIGN KEY (`redeemed_by_id`) REFERENCES `mc_application` (`id`),
  CONSTRAINT `refund_code_id_refs_id_1d7938b8e3e5b218` FOREIGN KEY (`refund_code_id`) REFERENCES `mc_refundcode` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9536 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_scenario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `stage_id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `description` longtext NOT NULL,
  `sequence_number` int(10) unsigned DEFAULT NULL,
  `panel_size` int(11) NOT NULL,
  `max_panels_per_judge` int(11) DEFAULT NULL,
  `min_panels_per_judge` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_scenario_name_47e6539550bf6955_uniq` (`name`,`stage_id`),
  UNIQUE KEY `mc_scenario_sequence_number_a97fc5cc088e606_uniq` (`sequence_number`,`stage_id`),
  KEY `mc_scenario_a8114449` (`stage_id`),
  CONSTRAINT `stage_id_refs_id_2b43640927983420` FOREIGN KEY (`stage_id`) REFERENCES `mc_judgingroundstage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=243 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_scenarioapplication` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_id` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `priority` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_scenarioapplication_scenario_id_163e3335590fe4d2_uniq` (`scenario_id`,`application_id`),
  KEY `mc_scenarioapplication_398529ef` (`application_id`),
  KEY `mc_scenarioapplication_3bb529ba` (`scenario_id`),
  CONSTRAINT `application_id_refs_id_eba383b8b909f05` FOREIGN KEY (`application_id`) REFERENCES `mc_application` (`id`),
  CONSTRAINT `scenario_id_refs_id_2f17d7079a08ad7a` FOREIGN KEY (`scenario_id`) REFERENCES `mc_scenario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=110598 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_scenariojudge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judge_id` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_scenariojudge_scenario_id_67fa0bcd38d447be_uniq` (`scenario_id`,`judge_id`),
  KEY `mc_scenariojudge_bcb024b0` (`judge_id`),
  KEY `mc_scenariojudge_3bb529ba` (`scenario_id`),
  CONSTRAINT `judge_id_refs_id_3d860029a0e7ae4e` FOREIGN KEY (`judge_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `scenario_id_refs_id_3352d89512fa5faf` FOREIGN KEY (`scenario_id`) REFERENCES `mc_scenario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68358 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_scenariopreference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scenario_id` int(11) NOT NULL,
  `priority` int(10) unsigned NOT NULL,
  `constraint_type` varchar(16) NOT NULL,
  `entity_type` varchar(16) NOT NULL,
  `entity_set` varchar(32) NOT NULL,
  `amount` int(10) unsigned DEFAULT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_scenariopreference_scenario_id_2e5f7d3baec37a3e_uniq` (`scenario_id`,`priority`,`entity_type`),
  KEY `mc_scenariopreference_3bb529ba` (`scenario_id`),
  CONSTRAINT `scenario_id_refs_id_778a93ab767dedb6` FOREIGN KEY (`scenario_id`) REFERENCES `mc_scenario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=691 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_section` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `heading` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `include_for` varchar(32) NOT NULL,
  `newsletter_id` int(11) NOT NULL,
  `sequence` int(10) unsigned NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_section_50580fc3` (`newsletter_id`),
  CONSTRAINT `newsletter_id_refs_id_5cc0bc71be6b4b70` FOREIGN KEY (`newsletter_id`) REFERENCES `mc_newsletter` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2293 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_section_interest_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `section_id` int(11) NOT NULL,
  `interestcategory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_section_interest_categories_section_id_7ae83d6e54a7dfb0_uniq` (`section_id`,`interestcategory_id`),
  KEY `mc_section_interest_categories_c007bd5a` (`section_id`),
  KEY `mc_section_interest_categories_3ba61f0a` (`interestcategory_id`),
  CONSTRAINT `mc_section_interest_section_id_6765b81994ce53ca_fk_mc_section_id` FOREIGN KEY (`section_id`) REFERENCES `mc_section` (`id`),
  CONSTRAINT `m_interestcategory_id_180b63e6adfab486_fk_mc_interestcategory_id` FOREIGN KEY (`interestcategory_id`) REFERENCES `mc_interestcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1848 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `security_key` varchar(100) NOT NULL,
  `description` varchar(500) NOT NULL,
  `site_url` varchar(200) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_siteprogramauthorization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `startup_list` tinyint(1) NOT NULL,
  `startup_profiles` tinyint(1) NOT NULL,
  `mentor_list` tinyint(1) NOT NULL,
  `videos` tinyint(1) NOT NULL,
  `sponsor_list` tinyint(1) NOT NULL,
  `sponsor_profiles` tinyint(1) NOT NULL,
  `sponsor_logos` tinyint(1) NOT NULL,
  `jobs` tinyint(1) NOT NULL,
  `startup_profile_base_url` varchar(200) NOT NULL,
  `sponsor_profile_base_url` varchar(200) NOT NULL,
  `video_base_url` varchar(200) NOT NULL,
  `startup_team_members` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_siteprogramauthorization_site_id_6d23da31460b4b00_uniq` (`site_id`,`program_id`),
  KEY `mc_siteprogramauthorization_6223029` (`site_id`),
  KEY `mc_siteprogramauthorization_7eef53e3` (`program_id`),
  CONSTRAINT `program_id_refs_id_973861a90a3d578` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `site_id_refs_id_23b3a0e24e71edc2` FOREIGN KEY (`site_id`) REFERENCES `mc_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `primary_industry_id` int(11) NOT NULL,
  `short_pitch` varchar(140) NOT NULL,
  `full_elevator_pitch` longtext NOT NULL,
  `website_url` varchar(100) NOT NULL,
  `linked_in_url` varchar(100) NOT NULL,
  `facebook_url` varchar(100) NOT NULL,
  `twitter_handle` varchar(40) NOT NULL,
  `public_inquiry_email` varchar(100) NOT NULL,
  `video_elevator_pitch_url` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `high_resolution_logo` varchar(100) NOT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_updated_datetime` datetime DEFAULT NULL,
  `community` varchar(64) NOT NULL,
  `url_slug` varchar(64) NOT NULL,
  `profile_background_color` varchar(7) NOT NULL,
  `profile_text_color` varchar(7) NOT NULL,
  `currency_id` int(11) DEFAULT NULL,
  `date_founded` varchar(100) NOT NULL,
  `location_city` varchar(100) NOT NULL,
  `location_national` varchar(100) NOT NULL,
  `location_postcode` varchar(100) NOT NULL,
  `location_regional` varchar(100) NOT NULL,
  `landing_page` varchar(255) DEFAULT NULL,
  `is_visible` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_startup_url_slug_4307d276937cb2aa_uniq` (`url_slug`),
  KEY `mc_startup_a7244bad` (`primary_industry_id`),
  KEY `user_id_refs_id_6b1225c67f892f18` (`user_id`),
  KEY `mc_startup_2c7d5721` (`currency_id`),
  CONSTRAINT `mc_startup_currency_id_a24d833928e93ed_fk_mc_currency_id` FOREIGN KEY (`currency_id`) REFERENCES `mc_currency` (`id`),
  CONSTRAINT `primary_industry_id_refs_id_7d0873860d6c0085` FOREIGN KEY (`primary_industry_id`) REFERENCES `mc_industry` (`id`),
  CONSTRAINT `user_id_refs_id_6b1225c67f892f18` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14223 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startup_recommendation_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `recommendationtag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_startup_recommendation_tags_startup_id_7c5983575634af26_uniq` (`startup_id`,`recommendationtag_id`),
  KEY `mc_startup_recommendation_tags_92fe01c8` (`startup_id`),
  KEY `mc_startup_recommendation_tags_d1dd995a` (`recommendationtag_id`),
  CONSTRAINT `mc_startup_recommen_startup_id_67290c17cb7f6e48_fk_mc_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`),
  CONSTRAINT `D7ab1977348253f6d99fd15b574561b2` FOREIGN KEY (`recommendationtag_id`) REFERENCES `mc_recommendationtag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=178492 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startup_related_industry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_startup_related_industry_startup_id_30c98f9faa444c3c_uniq` (`startup_id`,`industry_id`),
  KEY `mc_startup_related_industry_92fe01c8` (`startup_id`),
  KEY `mc_startup_related_industry_d28c39ae` (`industry_id`),
  CONSTRAINT `industry_id_refs_id_430002dc9e13d1c5` FOREIGN KEY (`industry_id`) REFERENCES `mc_industry` (`id`),
  CONSTRAINT `startup_id_refs_id_21523da37fa20883` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70141 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupattribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `attribute_id` int(11) NOT NULL,
  `attribute_value` longtext NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_startupattribute_92fe01c8` (`startup_id`),
  KEY `mc_startupattribute_f2eca69f` (`attribute_id`),
  CONSTRAINT `attribute_id_refs_id_65fe351d295bce44` FOREIGN KEY (`attribute_id`) REFERENCES `mc_programstartupattribute` (`id`),
  CONSTRAINT `startup_id_refs_id_63642cda78edc0e` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1802 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupcycleinterest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cycle_id` int(11) NOT NULL,
  `startup_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_startupcyclei_cycle_id_63ec9117ac740358_fk_mc_programcycle_id` (`cycle_id`),
  KEY `mc_startupcycleinte_startup_id_2b9d8c84ce38794f_fk_mc_startup_id` (`startup_id`),
  CONSTRAINT `mc_startupcycleinte_startup_id_2b9d8c84ce38794f_fk_mc_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`),
  CONSTRAINT `mc_startupcyclei_cycle_id_63ec9117ac740358_fk_mc_programcycle_id` FOREIGN KEY (`cycle_id`) REFERENCES `mc_programcycle` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20137 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startuplabel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `label` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startuplabel_startups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startuplabel_id` int(11) NOT NULL,
  `startup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `startuplabel_id` (`startuplabel_id`,`startup_id`),
  KEY `mc_startuplabel_sta_startup_id_33e8a0b43d2fac53_fk_mc_startup_id` (`startup_id`),
  CONSTRAINT `mc_startuplabel_sta_startup_id_33e8a0b43d2fac53_fk_mc_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`),
  CONSTRAINT `mc_startu_startuplabel_id_4ec94364338d2284_fk_mc_startuplabel_id` FOREIGN KEY (`startuplabel_id`) REFERENCES `mc_startuplabel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3509 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupmentorrelationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_mentor_tracking_id` int(11) NOT NULL,
  `mentor_id` int(11) NOT NULL,
  `status` varchar(32) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_startupmentorrelationship_e3c64f20` (`startup_mentor_tracking_id`),
  KEY `mc_startupmentorrelationship_cea652a7` (`mentor_id`),
  CONSTRAINT `mentor_id_refs_id_69fb20af11568f5f` FOREIGN KEY (`mentor_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `startup_mentor_tracking_id_refs_id_19c20b4e238d9343` FOREIGN KEY (`startup_mentor_tracking_id`) REFERENCES `mc_startupmentortrackingrecord` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3479 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupmentortrackingrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `other_mentors` longtext,
  `notes` longtext,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_startupmentortrackingrecord_startup_id_10b8df6326e8e6ae_uniq` (`startup_id`,`program_id`),
  KEY `mc_startupmentortrackingrecord_92fe01c8` (`startup_id`),
  KEY `mc_startupmentortrackingrecord_7eef53e3` (`program_id`),
  CONSTRAINT `program_id_refs_id_32b32b35fc16168b` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `startup_id_refs_id_174176547e67ac4` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=775 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupoverridegrant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `program_override_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_startupoverridegrant_92fe01c8` (`startup_id`),
  KEY `mc_startupoverridegrant_77a6cd5` (`program_override_id`),
  CONSTRAINT `program_override_id_refs_id_9ba554d03c6fe87` FOREIGN KEY (`program_override_id`) REFERENCES `mc_programoverride` (`id`),
  CONSTRAINT `startup_id_refs_id_349d7aa842b698c8` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupprograminterest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order` int(10) unsigned NOT NULL,
  `applying` tinyint(1) NOT NULL,
  `interest_level` varchar(64) DEFAULT NULL,
  `program_id` int(11) NOT NULL,
  `startup_id` int(11) NOT NULL,
  `startup_cycle_interest_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mc_startupprogramin_program_id_730ba2c52b7dc808_fk_mc_program_id` (`program_id`),
  KEY `mc_startupprogramin_startup_id_2d6e53cf28ee4903_fk_mc_startup_id` (`startup_id`),
  KEY `mc_startupprograminterest_70a17ffa` (`order`),
  KEY `mc_startupprograminterest_f699e0e2` (`startup_cycle_interest_id`),
  CONSTRAINT `c708cc6a4ef0a7fed91a1149d2bcbf3c` FOREIGN KEY (`startup_cycle_interest_id`) REFERENCES `mc_startupcycleinterest` (`id`),
  CONSTRAINT `mc_startupprogramin_program_id_730ba2c52b7dc808_fk_mc_program_id` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `mc_startupprogramin_startup_id_2d6e53cf28ee4903_fk_mc_startup_id` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46807 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startuprole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `program_startup_status_id` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_startupstatus_startup_id_12a679a3af235aad_uniq` (`startup_id`,`program_startup_status_id`),
  KEY `mc_startupstatus_92fe01c8` (`startup_id`),
  KEY `mc_startupstatus_4c64f505` (`program_startup_status_id`),
  CONSTRAINT `program_startup_status_id_refs_id_164be8ec89b9f8d0` FOREIGN KEY (`program_startup_status_id`) REFERENCES `mc_programstartupstatus` (`id`),
  CONSTRAINT `startup_id_refs_id_112519582f25807d` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37875 DEFAULT CHARSET=latin1;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupteammember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startup_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `startup_administrator` tinyint(1) NOT NULL,
  `is_contact` tinyint(1) NOT NULL,
  `technical_contact` tinyint(1) NOT NULL,
  `marketing_contact` tinyint(1) NOT NULL,
  `financial_contact` tinyint(1) NOT NULL,
  `legal_contact` tinyint(1) NOT NULL,
  `product_contact` tinyint(1) NOT NULL,
  `design_contact` tinyint(1) NOT NULL,
  `title` varchar(60) NOT NULL,
  `display_on_public_profile` tinyint(1) NOT NULL,
  `founder` tinyint(1) DEFAULT NULL,
  `primary_contact` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_startupteammember_startup_id_238984adddc26700_uniq` (`startup_id`,`user_id`),
  KEY `mc_startupteammember_92fe01c8` (`startup_id`),
  KEY `mc_startupteammember_fbfc09f1` (`user_id`),
  CONSTRAINT `startup_id_refs_id_56d2f0da5502cce8` FOREIGN KEY (`startup_id`) REFERENCES `mc_startup` (`id`),
  CONSTRAINT `user_id_refs_id_45c6fbdd2ad623d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25574 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_startupteammember_recommendation_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startupteammember_id` int(11) NOT NULL,
  `recommendationtag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_startupteammember_startupteammember_id_4654591bbb270440_uniq` (`startupteammember_id`,`recommendationtag_id`),
  KEY `mc_startupteammember_recommendation_tags_7486611` (`startupteammember_id`),
  KEY `mc_startupteammember_recommendation_tags_d1dd995a` (`recommendationtag_id`),
  CONSTRAINT `D274687269a1a79c1b5809450de49130` FOREIGN KEY (`recommendationtag_id`) REFERENCES `mc_recommendationtag` (`id`),
  CONSTRAINT `d576b6ac2dba85a9496621cfa7a87d28` FOREIGN KEY (`startupteammember_id`) REFERENCES `mc_startupteammember` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_us_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_userlabel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `label` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_userlabel_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userlabel_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `userlabel_id` (`userlabel_id`,`user_id`),
  KEY `mc_userlabel_users_user_id_6933accf268979f0_fk_auth_user_id` (`user_id`),
  CONSTRAINT `mc_userlabel_users_user_id_6933accf268979f0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `mc_userlabel_us_userlabel_id_50cdfbb02f325003_fk_mc_userlabel_id` FOREIGN KEY (`userlabel_id`) REFERENCES `mc_userlabel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15356 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `drupal_id` int(11) DEFAULT NULL,
  `linkedin_profile_link` varchar(255) NOT NULL,
  `judge_group` varchar(10) NOT NULL,
  `primary_industry` varchar(40) NOT NULL,
  `privacy_policy_accepted` tinyint(1) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_3f1ac0f92760bfe1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_userrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `url_slug` varchar(30) NOT NULL,
  `sort_order` int(10) unsigned NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(80) NOT NULL,
  `description` varchar(500) NOT NULL,
  `date` datetime DEFAULT NULL,
  `featured` tinyint(1) NOT NULL,
  `video_source_url` varchar(100) NOT NULL,
  `thumbnail_url` varchar(100) NOT NULL,
  `sort_weight` int(11) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_video_a951d5d6` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=209 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_video_video_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` int(11) NOT NULL,
  `videocategory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mc_video_video_categories_video_id_677b6cb355590480_uniq` (`video_id`,`videocategory_id`),
  KEY `mc_video_video_categories_fa26288c` (`video_id`),
  KEY `mc_video_video_categories_5f41b138` (`videocategory_id`),
  CONSTRAINT `mc_video_video_categori_video_id_60d2755004800b5c_fk_mc_video_id` FOREIGN KEY (`video_id`) REFERENCES `mc_video` (`id`),
  CONSTRAINT `mc_vide_videocategory_id_27db71ef91b2dfe8_fk_mc_videocategory_id` FOREIGN KEY (`videocategory_id`) REFERENCES `mc_videocategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=375 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mc_videocategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `program_id` int(11) NOT NULL,
  `public` tinyint(1) NOT NULL,
  `sort_weight` int(11) NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  PRIMARY KEY (`id`),
  KEY `mc_videocategory_a951d5d6` (`slug`),
  KEY `mc_videocategory_7eef53e3` (`program_id`),
  CONSTRAINT `program_id_refs_id_280186671e3ebb06` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagetype_fluentpage_fluentpage` (
  `urlnode_ptr_id` int(11) NOT NULL,
  `layout_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`urlnode_ptr_id`),
  KEY `pagetype_fluentpage_fluentpage_bf7cc574` (`layout_id`),
  CONSTRAINT `layout_id_refs_id_58475f64` FOREIGN KEY (`layout_id`) REFERENCES `fluent_pages_pagelayout` (`id`),
  CONSTRAINT `urlnode_ptr_id_refs_id_63eeaebf7631bd71` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagetype_mc_categoryheaderpage` (
  `urlnode_ptr_id` int(11) NOT NULL,
  `is_category_header` tinyint(1) NOT NULL,
  PRIMARY KEY (`urlnode_ptr_id`),
  CONSTRAINT `urlnode_ptr_id_refs_id_3840110913794bb5` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagetype_mc_filepage` (
  `urlnode_ptr_id` int(11) NOT NULL,
  `file` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`urlnode_ptr_id`),
  CONSTRAINT `urlnode_ptr_id_refs_id_377f6c6f6024dc4c` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagetype_mc_siteredirectpage` (
  `urlnode_ptr_id` int(11) NOT NULL,
  `new_url` varchar(100) NOT NULL,
  PRIMARY KEY (`urlnode_ptr_id`),
  CONSTRAINT `urlnode_ptr_id_refs_id_468c11ed732a5359` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagetype_mc_userrolemenu` (
  `urlnode_ptr_id` int(11) NOT NULL,
  `program_status` varchar(64) DEFAULT NULL,
  `program_family_id` int(11) DEFAULT NULL,
  `user_role_id` int(11) DEFAULT NULL,
  `program_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`urlnode_ptr_id`),
  KEY `pagetyp_program_family_id_c6e7ccad603a44c_fk_mc_programfamily_id` (`program_family_id`),
  KEY `pagetype_mc_user_user_role_id_6cac5fbcc4d13adc_fk_mc_userrole_id` (`user_role_id`),
  KEY `pagetype_mc_userrolemenu_429b1823` (`program_id`),
  CONSTRAINT `pagetype_mc_userrol_program_id_7eeaf62a8a1e191a_fk_mc_program_id` FOREIGN KEY (`program_id`) REFERENCES `mc_program` (`id`),
  CONSTRAINT `pagetype_mc_user_user_role_id_6cac5fbcc4d13adc_fk_mc_userrole_id` FOREIGN KEY (`user_role_id`) REFERENCES `mc_userrole` (`id`),
  CONSTRAINT `pagetyp_program_family_id_c6e7ccad603a44c_fk_mc_programfamily_id` FOREIGN KEY (`program_family_id`) REFERENCES `mc_programfamily` (`id`),
  CONSTRAINT `paget_urlnode_ptr_id_2f39dc373fe22072_fk_fluent_pages_urlnode_id` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagetype_redirectnode_redirectnode` (
  `urlnode_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`urlnode_ptr_id`),
  CONSTRAINT `urlnode_ptr_id_refs_id_57ddddca8208216b` FOREIGN KEY (`urlnode_ptr_id`) REFERENCES `fluent_pages_urlnode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypal_nvp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `method` varchar(64) NOT NULL,
  `ack` varchar(32) NOT NULL,
  `profilestatus` varchar(32) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `profileid` varchar(32) NOT NULL,
  `profilereference` varchar(128) NOT NULL,
  `correlationid` varchar(32) NOT NULL,
  `token` varchar(64) NOT NULL,
  `payerid` varchar(64) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `countrycode` varchar(2) NOT NULL,
  `zip` varchar(32) NOT NULL,
  `invnum` varchar(255) NOT NULL,
  `custom` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `flag` tinyint(1) NOT NULL,
  `flag_code` varchar(32) NOT NULL,
  `flag_info` longtext NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `query` longtext NOT NULL,
  `response` longtext NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paypal_nvp_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_c99b5482` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypal_pdt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `business` varchar(127) NOT NULL,
  `charset` varchar(255) NOT NULL,
  `custom` varchar(255) NOT NULL,
  `notify_version` decimal(64,2) DEFAULT NULL,
  `parent_txn_id` varchar(19) NOT NULL,
  `receiver_email` varchar(254) NOT NULL,
  `receiver_id` varchar(255) NOT NULL,
  `residence_country` varchar(2) NOT NULL,
  `test_ipn` tinyint(1) NOT NULL,
  `txn_id` varchar(255) NOT NULL,
  `txn_type` varchar(255) NOT NULL,
  `verify_sign` varchar(255) NOT NULL,
  `address_country` varchar(64) NOT NULL,
  `address_city` varchar(40) NOT NULL,
  `address_country_code` varchar(64) NOT NULL,
  `address_name` varchar(128) NOT NULL,
  `address_state` varchar(40) NOT NULL,
  `address_status` varchar(255) NOT NULL,
  `address_street` varchar(200) NOT NULL,
  `address_zip` varchar(20) NOT NULL,
  `contact_phone` varchar(20) NOT NULL,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `payer_business_name` varchar(127) NOT NULL,
  `payer_email` varchar(127) NOT NULL,
  `payer_id` varchar(13) NOT NULL,
  `auth_amount` decimal(64,2) DEFAULT NULL,
  `auth_exp` varchar(28) NOT NULL,
  `auth_id` varchar(19) NOT NULL,
  `auth_status` varchar(255) NOT NULL,
  `exchange_rate` decimal(64,16) DEFAULT NULL,
  `invoice` varchar(127) NOT NULL,
  `item_name` varchar(127) NOT NULL,
  `item_number` varchar(127) NOT NULL,
  `mc_currency` varchar(32) NOT NULL,
  `mc_fee` decimal(64,2) DEFAULT NULL,
  `mc_gross` decimal(64,2) DEFAULT NULL,
  `mc_handling` decimal(64,2) DEFAULT NULL,
  `mc_shipping` decimal(64,2) DEFAULT NULL,
  `memo` varchar(255) NOT NULL,
  `num_cart_items` int(11) DEFAULT NULL,
  `option_name1` varchar(64) NOT NULL,
  `option_name2` varchar(64) NOT NULL,
  `payer_status` varchar(255) NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `payment_gross` decimal(64,2) DEFAULT NULL,
  `payment_status` varchar(255) NOT NULL,
  `payment_type` varchar(255) NOT NULL,
  `pending_reason` varchar(255) NOT NULL,
  `protection_eligibility` varchar(255) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `reason_code` varchar(255) NOT NULL,
  `remaining_settle` decimal(64,2) DEFAULT NULL,
  `settle_amount` decimal(64,2) DEFAULT NULL,
  `settle_currency` varchar(32) NOT NULL,
  `shipping` decimal(64,2) DEFAULT NULL,
  `shipping_method` varchar(255) NOT NULL,
  `tax` decimal(64,2) DEFAULT NULL,
  `transaction_entity` varchar(255) NOT NULL,
  `auction_buyer_id` varchar(64) NOT NULL,
  `auction_closing_date` datetime DEFAULT NULL,
  `auction_multi_item` int(11) DEFAULT NULL,
  `for_auction` decimal(64,2) DEFAULT NULL,
  `amount` decimal(64,2) DEFAULT NULL,
  `amount_per_cycle` decimal(64,2) DEFAULT NULL,
  `initial_payment_amount` decimal(64,2) DEFAULT NULL,
  `next_payment_date` datetime DEFAULT NULL,
  `outstanding_balance` decimal(64,2) DEFAULT NULL,
  `payment_cycle` varchar(255) NOT NULL,
  `period_type` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_type` varchar(255) NOT NULL,
  `profile_status` varchar(255) NOT NULL,
  `recurring_payment_id` varchar(255) NOT NULL,
  `rp_invoice_id` varchar(127) NOT NULL,
  `time_created` datetime DEFAULT NULL,
  `amount1` decimal(64,2) DEFAULT NULL,
  `amount2` decimal(64,2) DEFAULT NULL,
  `amount3` decimal(64,2) DEFAULT NULL,
  `mc_amount1` decimal(64,2) DEFAULT NULL,
  `mc_amount2` decimal(64,2) DEFAULT NULL,
  `mc_amount3` decimal(64,2) DEFAULT NULL,
  `password` varchar(24) NOT NULL,
  `period1` varchar(255) NOT NULL,
  `period2` varchar(255) NOT NULL,
  `period3` varchar(255) NOT NULL,
  `reattempt` varchar(1) NOT NULL,
  `recur_times` int(11) DEFAULT NULL,
  `recurring` varchar(1) NOT NULL,
  `retry_at` datetime DEFAULT NULL,
  `subscr_date` datetime DEFAULT NULL,
  `subscr_effective` datetime DEFAULT NULL,
  `subscr_id` varchar(19) NOT NULL,
  `username` varchar(64) NOT NULL,
  `case_creation_date` datetime DEFAULT NULL,
  `case_id` varchar(255) NOT NULL,
  `case_type` varchar(255) NOT NULL,
  `receipt_id` varchar(255) NOT NULL,
  `currency_code` varchar(32) NOT NULL,
  `handling_amount` decimal(64,2) DEFAULT NULL,
  `transaction_subject` varchar(255) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `flag` tinyint(1) NOT NULL,
  `flag_code` varchar(16) NOT NULL,
  `flag_info` longtext NOT NULL,
  `query` longtext NOT NULL,
  `response` longtext NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `from_view` varchar(6) DEFAULT NULL,
  `amt` decimal(64,2) DEFAULT NULL,
  `cm` varchar(255) NOT NULL,
  `sig` varchar(255) NOT NULL,
  `tx` varchar(255) NOT NULL,
  `st` varchar(32) NOT NULL,
  `mp_id` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redirectnode_redirectnode_translation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_code` varchar(15) NOT NULL,
  `new_url` varchar(255) NOT NULL,
  `redirect_type` int(11) NOT NULL,
  `master_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `redirectnode_redirectnode_t_language_code_5baf240a84e8cda8_uniq` (`language_code`,`master_id`),
  KEY `redirectnode_redirectnode_translation_da473cdf` (`language_code`),
  KEY `redirectnode_redirectnode_translation_11a5708d` (`master_id`),
  CONSTRAINT `master_id_refs_urlnode_ptr_id_e8de4203` FOREIGN KEY (`master_id`) REFERENCES `pagetype_redirectnode_redirectnode` (`urlnode_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_registrationprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `activation_key` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_cecd7f3c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37370 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `thumbnail_kvstore` (
  `key` varchar(200) NOT NULL,
  `value` longtext NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `actstream_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `actor_object_id` varchar(255) NOT NULL,
  `verb` varchar(255) NOT NULL,
  `description` longtext,
  `target_object_id` varchar(255) DEFAULT NULL,
  `action_object_object_id` varchar(255) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `public` tinyint(1) NOT NULL,
  `action_object_content_type_id` int(11) DEFAULT NULL,
  `actor_content_type_id` int(11) NOT NULL,
  `target_content_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `D31fae754d7fa426d7a05a50b9f0d82d` (`action_object_content_type_id`),
  KEY `dd469efd5a07c52e8e9bcb80a85b12ec` (`actor_content_type_id`),
  KEY `D0f72146799bb15634dae56ed418fd89` (`target_content_type_id`),
  KEY `actstream_action_c4f7c191` (`actor_object_id`),
  KEY `actstream_action_b512ddf1` (`verb`),
  KEY `actstream_action_1cd2a6ae` (`target_object_id`),
  KEY `actstream_action_9063443c` (`action_object_object_id`),
  KEY `actstream_action_d7e6d55b` (`timestamp`),
  KEY `actstream_action_4c9184f3` (`public`),
  CONSTRAINT `D0f72146799bb15634dae56ed418fd89` FOREIGN KEY (`target_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `D31fae754d7fa426d7a05a50b9f0d82d` FOREIGN KEY (`action_object_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `dd469efd5a07c52e8e9bcb80a85b12ec` FOREIGN KEY (`actor_content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=151124 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `actstream_follow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` varchar(255) NOT NULL,
  `actor_only` tinyint(1) NOT NULL,
  `started` datetime NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `actstream_follow_user_id_49f02cb6d67a13f2_uniq` (`user_id`,`content_type_id`,`object_id`),
  KEY `actst_content_type_id_30a29286dd004af8_fk_django_content_type_id` (`content_type_id`),
  KEY `actstream_follow_af31437c` (`object_id`),
  KEY `actstream_follow_3bebb2f8` (`started`),
  CONSTRAINT `actstream_follow_user_id_2dbe1c43431b23ab_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `actst_content_type_id_30a29286dd004af8_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `django_site` VALUES (1,'accelerate.masschallenge.org','MassChallenge.org');
