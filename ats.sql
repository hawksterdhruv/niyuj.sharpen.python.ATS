drop database ats;

create database ats;

CREATE TABLE IF NOT EXISTS `ats`.`employee` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `mobileno` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ats`.`candidate` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `skills` VARCHAR(255) NOT NULL,
  `experience` INT NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `mobileno` VARCHAR(10) NOT NULL,
  `source` VARCHAR(20) NULL,
  `reffered_by` INT DEFAULT 0,
  `resume` BLOB NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `current_ctc` INT NOT NULL DEFAULT 0,
  `expected_ctc` INT NOT NULL DEFAULT 0,
  `current_organization` VARCHAR(100) NULL,
  `notice_period` INT NULL DEFAULT 0,
  PRIMARY KEY (`id`,`reffered_by`),
  CONSTRAINT `referred_employee`
    FOREIGN KEY (`reffered_by`)
    REFERENCES `ats`.`employee` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ats`.`project` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
   PRIMARY KEY (`id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ats`.`job_position` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `project_id` INT NOT NULL,
  `employee_id` INT NOT NULL,
  `title` VARCHAR(50) NOT NULL,
  `experience` INT NOT NULL DEFAULT 0,
  `skills` VARCHAR(255) NULL,
  `no_of_openings` INT NOT NULL DEFAULT 0,
  `status` VARCHAR(30) NULL,
  `grade` VARCHAR(5) NOT NULL,
   PRIMARY KEY (`id`, `project_id`,`employee_id`),
   CONSTRAINT `project_job`
    FOREIGN KEY (`project_id`)
    REFERENCES `ats`.`project` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `project_employee`
    FOREIGN KEY (`employee_id`)
    REFERENCES `ats`.`employee` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ats`.`job_has_candidate` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `candidate_id` INT NOT NULL,
  `position_id` INT NOT NULL,
  PRIMARY KEY (`id`, `candidate_id`, `position_id`),
  UNIQUE INDEX `unique_link`(`candidate_id`, `position_id`),
   CONSTRAINT `fk1_job_has_candidate`
    FOREIGN KEY (`candidate_id`)
    REFERENCES `ats`.`candidate` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
   CONSTRAINT `fk2_job_has_candidate`
    FOREIGN KEY (`position_id`)
    REFERENCES `ats`.`job_position` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ats`.`interview` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `job_has_candidate_id` INT NOT NULL,
  `employee_id` INT NOT NULL,
  `channel` VARCHAR(55) NULL,
  `location` VARCHAR(55) NULL,
  `comment` VARCHAR(55) NULL,
  `feedback` VARCHAR(55) NULL,
  `schedule_time` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`, `job_has_candidate_id`, `employee_id`),
   CONSTRAINT `fk1_interview`
    FOREIGN KEY (`job_has_candidate_id`)
    REFERENCES `ats`.`job_has_candidate` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
   CONSTRAINT `fk2_interview`
    FOREIGN KEY (`employee_id`)
    REFERENCES `ats`.`employee` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
   
use ats;

INSERT INTO employee(id,name,email,address,mobileno) VALUES
(1,'rhishekesh','rhishekesh.magdum@niyuj.com','Hinjewadi,Pune','8890764732'),
(2,'supriya','supriya.karkhile@niyuj.com','Baner,PUne','1234567890');

INSERT INTO project(id,name) VALUES
(1,'Edgeview'),
(2,'EdgeMarc');
