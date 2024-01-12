CREATE TABLE `user` (
	`user_id`	int unsigned auto_increment	NOT NULL,
	`role`	char	NULL
);

CREATE TABLE `project_user` (
	`project_user_id`	int unsigned auto_increment	NOT NULL,
	`user_id2`	int unsigned auto_increment	NOT NULL,
	`passward`	varchar(20)	NULL,
	`nickname`	varchar(15)	NULL,
	`agree_TOS`	char	NULL,
	`status`	varchar(10)	NULL,
	`created_at`	timestamp DEFAULT current_timestamp	NULL,
	`updated_at`	timestamp DEFAULT current_timestamp	NULL,
	`company_name`	varchar(30)	NULL,
	`gender`	char	NULL,
	`birth`	date	NULL
);

CREATE TABLE `general_user` (
	`project_user_id`	int unsigned auto_increment	NOT NULL,
	`user_id2`	int unsigned auto_increment	NOT NULL,
	`passward`	varchar(20)	NULL,
	`nickname`	varchar(15)	NULL,
	`agree_TOS`	char	NULL,
	`status`	varchar(10)	NULL,
	`created_at`	timestamp DEFAULT current_timestamp	NULL,
	`updated_at`	timestamp DEFAULT current_timestamp	NULL,
	`gender`	char	NULL,
	`birth`	date	NULL
);

CREATE TABLE `question` (
	`question_id`	int unsigned auto_increment	NOT NULL,
	`question_created_date`	timestamp DEFAULT current_timestamp	NULL,
	`question_modified_date`	timestamp DEFAULT current_timestamp	NULL,
	`question_image`	varchar(255)	NULL,
	`question_content`	varchar(1000)	NULL,
	`question_title`	varchar(50)	NULL,
	`user_id`	int unsigned auto_increment	NOT NULL
);

CREATE TABLE `comment` (
	`comment_id`	int unsigned auto_increment	NOT NULL,
	`story_id`	int	NOT NULL,
	`content`	varchar(500)	NULL,
	`created_date`	timestamp DEFAULT current_timestamp	NULL,
	`modified_date`	timestamp DEFAULT current_timestamp	NULL,
	`user_id`	int unsigned auto_increment	NOT NULL
);

CREATE TABLE `story` (
	`story_id`	int unsigned auto_increment	NOT NULL,
	`created_date`	timestamp DEFAULT current_timestamp	NULL,
	`modified_date`	timestamp DEFAULT current_timestamp	NULL,
	`title`	varchar(50)	NULL,
	`content`	varchar(1000)	NULL,
	`category`	int	NULL,
	`image`	varchar(255)	NULL,
	`user_id`	int unsigned auto_increment	NOT NULL
);

CREATE TABLE `project` (
	`project_id`	int unsigned auto_increment	NOT NULL,
	`project_user_id`	int	NOT NULL,
	`title`	varchar(100)	NULL,
	`image`	text	NULL,
	`created_at`	timestamp DEFAULT current_timestamp	NULL,
	`updated_at`	timestamp DEFAULT current_timestamp	NULL,
	`project_detail`	varchar(300)	NULL,
	`project_name`	varchar(20)	NULL,
	`project_time`	int	NULL,
	`project_end`	date	NULL,
	`project_start`	date	NULL,
	`project_val`	varchar(10)	NULL,
	`project_peo`	int	NULL,
	`project_pm`	varchar(10)	NULL,
	`project_company`	varchar(20)	NULL,
	`project_ent`	boolean	NULL,
	`project_mov`	boolean	NULL,
	`project_promotion`	char	NULL,
	`project_num`	int	NULL,
	`project_emotion`	char	NULL
);

CREATE TABLE `participation_code` (
	`participation_id`	varchar(10)	NOT NULL,
	`project_id`	int	NOT NULL,
	`project_user_id`	int	NOT NULL
);

CREATE TABLE `project_count` (
	`project_count_id`	int unsigned auto_increment	NOT NULL,
	`user_id2`	int	NOT NULL,
	`project_id`	int	NOT NULL
);

CREATE TABLE `project_image` (
	`image_id`	int unsigned auto_increment	NOT NULL,
	`project_count_id`	int unsigned auto_increment	NOT NULL,
	`file_name`	varchar(255)	NULL,
	`created_at`	timestamp DEFAULT current_timestamp	NULL,
	`updated_at`	timestamp DEFAULT current_timestamp	NULL,
	`test_bool`	boolean	NULL,
	`movie_bool`	boolean	NULL
);

CREATE TABLE `biometric` (
	`bio_id`	int unsigned auto_increment	NOT NULL,
	`image_id`	int unsigned auto_increment	NOT NULL,
	`project_count_id`	int unsigned auto_increment	NOT NULL,
	`score`	int	NULL
);

ALTER TABLE `user` ADD CONSTRAINT `PK_USER` PRIMARY KEY (
	`user_id`
);

ALTER TABLE `project_user` ADD CONSTRAINT `PK_PROJECT_USER` PRIMARY KEY (
	`project_user_id`,
	`user_id2`
);

ALTER TABLE `general_user` ADD CONSTRAINT `PK_GENERAL_USER` PRIMARY KEY (
	`project_user_id`,
	`user_id2`
);

ALTER TABLE `question` ADD CONSTRAINT `PK_QUESTION` PRIMARY KEY (
	`question_id`
);

ALTER TABLE `comment` ADD CONSTRAINT `PK_COMMENT` PRIMARY KEY (
	`comment_id`,
	`story_id`
);

ALTER TABLE `story` ADD CONSTRAINT `PK_STORY` PRIMARY KEY (
	`story_id`
);

ALTER TABLE `project` ADD CONSTRAINT `PK_PROJECT` PRIMARY KEY (
	`project_id`,
	`project_user_id`
);

ALTER TABLE `participation_code` ADD CONSTRAINT `PK_PARTICIPATION_CODE` PRIMARY KEY (
	`participation_id`,
	`project_id`,
	`project_user_id`
);

ALTER TABLE `project_count` ADD CONSTRAINT `PK_PROJECT_COUNT` PRIMARY KEY (
	`project_count_id`
);

ALTER TABLE `project_image` ADD CONSTRAINT `PK_PROJECT_IMAGE` PRIMARY KEY (
	`image_id`,
	`project_count_id`
);

ALTER TABLE `biometric` ADD CONSTRAINT `PK_BIOMETRIC` PRIMARY KEY (
	`bio_id`,
	`image_id`,
	`project_count_id`
);

ALTER TABLE `project_user` ADD CONSTRAINT `FK_user_TO_project_user_1` FOREIGN KEY (
	`user_id2`
)
REFERENCES `user` (
	`user_id`
);

ALTER TABLE `general_user` ADD CONSTRAINT `FK_user_TO_general_user_1` FOREIGN KEY (
	`user_id2`
)
REFERENCES `user` (
	`user_id`
);

ALTER TABLE `comment` ADD CONSTRAINT `FK_story_TO_comment_1` FOREIGN KEY (
	`story_id`
)
REFERENCES `story` (
	`story_id`
);

ALTER TABLE `project` ADD CONSTRAINT `FK_project_user_TO_project_1` FOREIGN KEY (
	`project_user_id`
)
REFERENCES `project_user` (
	`project_user_id`
);

ALTER TABLE `participation_code` ADD CONSTRAINT `FK_project_TO_participation_code_1` FOREIGN KEY (
	`project_id`
)
REFERENCES `project` (
	`project_id`
);

ALTER TABLE `participation_code` ADD CONSTRAINT `FK_project_TO_participation_code_2` FOREIGN KEY (
	`project_user_id`
)
REFERENCES `project` (
	`project_user_id`
);

ALTER TABLE `project_image` ADD CONSTRAINT `FK_project_count_TO_project_image_1` FOREIGN KEY (
	`project_count_id`
)
REFERENCES `project_count` (
	`project_count_id`
);

ALTER TABLE `biometric` ADD CONSTRAINT `FK_project_image_TO_biometric_1` FOREIGN KEY (
	`image_id`
)
REFERENCES `project_image` (
	`image_id`
);

ALTER TABLE `biometric` ADD CONSTRAINT `FK_project_image_TO_biometric_2` FOREIGN KEY (
	`project_count_id`
)
REFERENCES `project_image` (
	`project_count_id`
);

