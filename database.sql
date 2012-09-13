/*
I wanted to keep tables simple.
This is not perfect table design.
*/

CREATE TABLE IF NOT EXISTS `Notifications` (
  `id` int(11) NOT NULL auto_increment,
  `title` text,
  `link` varchar(200) default NULL,
  `date` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=310 ;


CREATE TABLE IF NOT EXISTS `Timetable` (
  `id` int(11) NOT NULL auto_increment,
  `title` text,
  `link` varchar(200) default NULL,
  `date` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=310 ;

CREATE TABLE IF NOT EXISTS `Results` (
  `id` int(11) NOT NULL auto_increment,
  `title` text,
  `link` varchar(200) default NULL,
  `date` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=310 ;
