INSERT INTO User (username, firstname, lastname, password, email) VALUES
('sportslover', 'Paul', 'Walker', 'sha512$50a4ab0065e74e40b8c7293dcf570eec$b05b7dbae4c94f5ca360b0363bbcc6d160315ce3180ca0f6a6d5872de710aadbcefcb264d0d7371ddbedebd361a40886fc419540c2a4bcf023b27cb2b456c542', 'sportslover@hotmail.com'),
('traveler', 'Rebecca', 'Travolta', 'sha512$3bbf48fec0f145bc8e0840cf123e469a$702cd6e93d6626055d5efcdd113684faea3dbd652819c62ac5069d6052bc4cef23c4fb56d9405f5c0fe47e957b7ac5d5ee18331183cbad0c0c27b88eca6399c2', 'rebt@explorer.org'), 
('spacejunkie', 'Bob', 'Spacey', 'sha512$890c79e6c407444987f10d60dab3e0ae$94688c46368d1de0e1d61b3cefc43766bd8a40841402cba197625b2b20d670b69492ff5273df122437bc78b6d4a0a43167adc29c235fb12b7cb0d7b17450d09e', 'bspace@spacejunkies.net');

INSERT INTO Album (albumid, title, created, lastupdated, username, access) VALUES
(1, 'I love sports', NOW(), NOW(), 'sportslover', 'public'),
(2, 'I love football', NOW(), NOW(), 'sportslover', 'private'),
(3, 'Around The World', NOW(), NOW(), 'traveler', 'public'),
(4, 'Cool Space Shots', NOW(), NOW(), 'spacejunkie', 'private');

INSERT INTO Photo(picid, format) values("001025dd643b0eb0661e359de86e3ea9", "jpg"); 
INSERT INTO Photo(picid, format) values("9a0a7d25af4f7a73f67dde74e8e54cff", "jpg"); 
INSERT INTO Photo(picid, format) values("c8e60100f13ffe374d59e39dc4b6a318", "jpg"); 
INSERT INTO Photo(picid, format) values("5e8b6207f007338243d3e29d6b82acab", "jpg"); 
INSERT INTO Photo(picid, format) values("4ddba6e2f905e9778c6b6a48b6fc8e03", "jpg"); 
INSERT INTO Photo(picid, format) values("09d8a979fa638125b02ae1578eb943fa", "jpg"); 
INSERT INTO Photo(picid, format) values("143ba34cb5c7e8f12420be1b576bda1a", "jpg"); 
INSERT INTO Photo(picid, format) values("e615a10fc4222ede59ca3316c3fb751c", "jpg"); 
INSERT INTO Photo(picid, format) values("65fb1e2aa4977d9414d1b3a7e4a3badd", "jpg"); 
INSERT INTO Photo(picid, format) values("b94f256c23dec8a2c0da546849058d9e", "jpg"); 
INSERT INTO Photo(picid, format) values("01e37cbdd55913df563f527860b364e8", "jpg"); 
INSERT INTO Photo(picid, format) values("8d554cd1d8bb7b49ca798381d1fc171b", "jpg"); 
INSERT INTO Photo(picid, format) values("2e9e69e19342b98141789925e5f87f60", "jpg"); 
INSERT INTO Photo(picid, format) values("298e8943ef1942159ef88be21c4619c9", "jpg"); 
INSERT INTO Photo(picid, format) values("cefe45eaeaeb599256dda325c2e972da", "jpg"); 
INSERT INTO Photo(picid, format) values("bf755d13bb78e1deb59ef66b6d5c6a70", "jpg"); 
INSERT INTO Photo(picid, format) values("5f8d7957874f1303d8300e50f17e46d6", "jpg"); 
INSERT INTO Photo(picid, format) values("bac4fca50bed35b9a5646f632bf4c2e8", "jpg"); 
INSERT INTO Photo(picid, format) values("f5b57bd7a2c962c54d55b5ddece37158", "jpg"); 
INSERT INTO Photo(picid, format) values("b7d833dd3aae203ca618759fc6f4fc01", "jpg"); 
INSERT INTO Photo(picid, format) values("faa20c04097d40cb10793a19246f2754", "jpg"); 
INSERT INTO Photo(picid, format) values("aaaadd578c78d21defaa73e7d1f08235", "jpg"); 
INSERT INTO Photo(picid, format) values("adb5c3af19664129141268feda90a275", "jpg"); 
INSERT INTO Photo(picid, format) values("abf97ffd1f964f42790fb358e5258e8d", "jpg"); 
INSERT INTO Photo(picid, format) values("ea2db8b970671856e43dd011d7df5fad", "jpg"); 
INSERT INTO Photo(picid, format) values("76d79b81b9073a2323f0790965b00a68", "jpg"); 
INSERT INTO Photo(picid, format) values("6510a4add59ef655ae3f0b6cdb24e140", "jpg"); 
INSERT INTO Photo(picid, format) values("28d38afca913a728b2a6bcf01aa011cd", "jpg"); 
INSERT INTO Photo(picid, format) values("5fb04eb11cbf99429a05c12ce2f50615", "jpg"); 
INSERT INTO Photo(picid, format) values("39ee267d13ccd32b50c1de7c2ece54d6", "jpg");

INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (0,  2, "001025dd643b0eb0661e359de86e3ea9", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (1,  2, "9a0a7d25af4f7a73f67dde74e8e54cff", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (2,  2, "c8e60100f13ffe374d59e39dc4b6a318", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (3,  2, "5e8b6207f007338243d3e29d6b82acab", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (4,  4, "4ddba6e2f905e9778c6b6a48b6fc8e03", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (5,  4, "09d8a979fa638125b02ae1578eb943fa", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (6,  4, "143ba34cb5c7e8f12420be1b576bda1a", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (7,  4, "e615a10fc4222ede59ca3316c3fb751c", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (8,  4, "65fb1e2aa4977d9414d1b3a7e4a3badd", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (9,  1, "b94f256c23dec8a2c0da546849058d9e", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (10, 1, "01e37cbdd55913df563f527860b364e8", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (11, 1, "8d554cd1d8bb7b49ca798381d1fc171b", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (12, 1, "2e9e69e19342b98141789925e5f87f60", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (13, 1, "298e8943ef1942159ef88be21c4619c9", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (14, 1, "cefe45eaeaeb599256dda325c2e972da", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (15, 1, "bf755d13bb78e1deb59ef66b6d5c6a70", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (16, 1, "5f8d7957874f1303d8300e50f17e46d6", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (17, 3, "bac4fca50bed35b9a5646f632bf4c2e8", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (18, 3, "f5b57bd7a2c962c54d55b5ddece37158", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (19, 3, "b7d833dd3aae203ca618759fc6f4fc01", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (20, 3, "faa20c04097d40cb10793a19246f2754", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (21, 3, "aaaadd578c78d21defaa73e7d1f08235", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (22, 3, "adb5c3af19664129141268feda90a275", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (23, 3, "abf97ffd1f964f42790fb358e5258e8d", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (24, 3, "ea2db8b970671856e43dd011d7df5fad", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (25, 3, "76d79b81b9073a2323f0790965b00a68", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (26, 3, "6510a4add59ef655ae3f0b6cdb24e140", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (27, 3, "28d38afca913a728b2a6bcf01aa011cd", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (28, 3, "5fb04eb11cbf99429a05c12ce2f50615", ""); 
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (29, 3, "39ee267d13ccd32b50c1de7c2ece54d6", ""); 
