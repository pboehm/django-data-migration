CREATE TABLE `authors` (
  `id` INTEGER PRIMARY KEY,
  `Firstname` varchar(255) default NULL,
  `Lastname` varchar(255) default NULL,
  `EmailAdress` varchar(255) default NULL
);

INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Wade","Castillo","ante.Maecenas.mi@ornareInfaucibus.net");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Bernard","Marks","a.scelerisque.sed@ametmetus.net");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Wallace","Griffith","auctor.velit@mattis.edu");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Fuller","Knox","primis.in@egestasFusce.ca");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Nero","Wright","facilisis@Aliquamfringillacursus.edu");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Macon","Morse","ipsum@magnisdis.ca");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Evan","Durham","quam.quis.diam@luctuset.edu");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Talon","Gregory","iaculis@eratvolutpatNulla.org");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Scott","Rollins","Sed.neque@massaQuisqueporttitor.ca");
INSERT INTO `authors` (`Firstname`,`Lastname`,`EmailAdress`) VALUES ("Omar","Meyer","orci.luctus.et@urnaet.net");


CREATE TABLE `comments` (
  `id` INTEGER PRIMARY KEY,
  `Message` TEXT default NULL,
  `Author` mediumint default NULL,
  `PostedAt` varchar(255),
  `Post` mediumint default NULL
);

INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("eu nulla at sem molestie sodales. Mauris blandit enim consequat",4,"2013-09-18 23:36:56",7);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("magna. Sed eu eros. Nam consequat dolor vitae dolor. Donec fringilla.",1,"2014-09-29 04:36:50",2);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;",2,"2013-07-20 12:30:30",10);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("rutrum. Fusce dolor quam, elementum at, egestas a, scelerisque sed, sapien. Nunc pulvinar arcu",2,"2013-09-04 10:10:51",9);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("venenatis lacus. Etiam bibendum fermentum metus. Aenean sed pede nec ante",8,"2014-04-17 04:41:25",10);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("fringilla ornare placerat, orci lacus vestibulum lorem, sit amet ultricies sem magna nec",3,"2013-10-28 19:41:31",2);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("Nunc mauris sapien, cursus in, hendrerit consectetuer, cursus et, magna. Praesent",3,"2013-07-29 21:30:25",2);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("posuere vulputate, lacus. Cras interdum. Nunc sollicitudin commodo ipsum. Suspendisse non leo.",7,"2014-01-05 14:57:55",4);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("sem magna nec quam. Curabitur vel lectus. Cum sociis natoque penatibus",3,"2014-11-19 20:19:32",2);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("molestie pharetra nibh. Aliquam ornare, libero at auctor ullamcorper, nisl arcu iaculis enim, sit",8,"2013-03-07 04:49:44",7);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("sed turpis nec mauris blandit mattis. Cras eget nisi dictum augue malesuada malesuada. Integer id",1,"2013-09-05 17:28:40",4);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("scelerisque dui. Suspendisse ac metus vitae velit egestas lacinia. Sed congue, elit sed consequat",10,"2014-09-21 12:57:47",9);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna",6,"2014-12-17 13:08:00",9);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("ornare placerat, orci lacus vestibulum lorem, sit amet ultricies sem magna nec quam. Curabitur vel",3,"2013-07-01 18:30:22",7);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("in, hendrerit consectetuer, cursus et, magna. Praesent interdum ligula eu enim. Etiam imperdiet dictum",2,"2014-08-25 17:47:44",1);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("malesuada id, erat. Etiam vestibulum massa rutrum magna. Cras convallis convallis dolor.",10,"2014-01-17 11:11:40",4);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("tempor arcu. Vestibulum ut eros non enim commodo hendrerit. Donec porttitor tellus non",3,"2013-11-22 05:31:30",7);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("porta elit, a feugiat tellus lorem eu metus. In lorem. Donec",3,"2013-07-20 01:33:08",6);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("ipsum porta elit, a feugiat tellus lorem eu metus. In lorem.",10,"2013-12-20 17:48:11",7);
INSERT INTO `comments` (`Message`,`Author`,`PostedAt`,`Post`) VALUES ("et, magna. Praesent interdum ligula eu enim. Etiam imperdiet dictum magna. Ut tincidunt orci quis",4,"2014-08-05 08:58:54",4);


CREATE TABLE `posts` (
  `id` INTEGER PRIMARY KEY,
  `Title` TEXT default NULL,
  `Body` TEXT default NULL,
  `Posted` varchar(255),
  `Author` mediumint default NULL
);

INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("parturient montes, nascetur ridiculus mus. Aenean eget magna. Suspendisse tristique","ullamcorper eu, euismod ac, fermentum vel, mauris. Integer sem elit, pharetra ut, pharetra sed, hendrerit a, arcu. Sed et libero. Proin","2014-03-08 05:22:35",10);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("congue, elit sed consequat auctor, nunc nulla vulputate dui, nec","feugiat non, lobortis quis, pede. Suspendisse dui. Fusce diam nunc, ullamcorper eu, euismod ac, fermentum vel, mauris. Integer sem elit, pharetra ut, pharetra sed, hendrerit a, arcu. Sed et libero.","2013-11-21 09:29:19",10);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("Phasellus libero mauris, aliquam eu, accumsan sed, facilisis vitae, orci.","Donec vitae erat vel pede blandit congue. In scelerisque scelerisque dui. Suspendisse ac metus vitae velit egestas lacinia. Sed congue, elit sed consequat auctor, nunc nulla vulputate dui, nec tempus","2013-05-25 11:56:59",5);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("et arcu imperdiet ullamcorper. Duis at lacus. Quisque purus sapien,","egestas. Aliquam fringilla cursus purus. Nullam scelerisque neque sed sem egestas blandit. Nam nulla magna, malesuada","2013-12-30 06:29:06",9);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("est mauris, rhoncus id, mollis nec, cursus a, enim. Suspendisse","aliquet odio. Etiam ligula tortor, dictum eu, placerat eget, venenatis a, magna. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Etiam laoreet, libero","2014-01-30 04:37:36",10);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("mollis dui, in sodales elit erat vitae risus. Duis a","Maecenas malesuada fringilla est. Mauris eu turpis. Nulla aliquet. Proin velit. Sed malesuada augue ut lacus. Nulla tincidunt, neque vitae semper egestas, urna justo faucibus lectus,","2014-05-16 04:11:51",10);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("amet, risus. Donec nibh enim, gravida sit amet, dapibus id,","ut mi. Duis risus odio, auctor vitae, aliquet nec, imperdiet nec, leo. Morbi neque tellus, imperdiet non, vestibulum nec, euismod in, dolor.","2014-08-11 16:53:25",1);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("erat, eget tincidunt dui augue eu tellus. Phasellus elit pede,","Nunc ullamcorper, velit in aliquet lobortis, nisi nibh lacinia orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc quis arcu vel quam dignissim pharetra.","2014-03-18 18:02:49",1);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("lacinia at, iaculis quis, pede. Praesent eu dui. Cum sociis","faucibus id, libero. Donec consectetuer mauris id sapien. Cras dolor dolor, tempus non, lacinia at, iaculis quis, pede. Praesent eu dui. Cum sociis natoque penatibus et magnis dis parturient montes,","2014-10-13 08:36:59",8);
INSERT INTO `posts` (`Title`,`Body`,`Posted`,`Author`) VALUES ("rutrum eu, ultrices sit amet, risus. Donec nibh enim, gravida","Proin nisl sem, consequat nec, mollis vitae, posuere at, velit. Cras lorem lorem, luctus ut, pellentesque eget, dictum placerat, augue. Sed molestie. Sed id risus","2013-03-22 08:49:01",8);
