INSERT INTO movies.movies (movie_title, movie_description, release_year, runtime_minutes, rating, votes, revenue_millions, metascore)
Values
('Prometheus','Following clues to the origin of mankind, a team finds a structure on a distant moon, but they soon realize they are not alone.', 2012,124,7,485820,126.46,65)
('Split', 'Three girls are kidnapped by a man with a diagnosed 23 distinct personalities. They must try to escape before the apparent emergence of a frightful new 24th.', 2016,117,7.3,157606,138.12,62)
('Sing', 'In a city of humanoid animals, a hustling theater impresario''s attempt to save his theater with a singing competition becomes grander than he anticipates even as its finalists find that their lives will never be the same.', 2016, 108, 7.2, 605.45, 270.32, 59)
('Suicide Squad', 'A secret government agency recruits some of the most dangerous incarcerated super-villains to form a defensive task force. Their first mission: save the world from the apocalypse.', 2016, 123, 6.2, 393727, 325.02, 40)
( 'The Great Wall', 'European mercenaries searching for black powder become embroiled in the defense of the Great Wall of China against a horde of monstrous creatures.', 2016, 103, 6.1, 56036, 45.13, 42)
( 'La La Land', 'A jazz pianist falls for an aspiring actress in Los Angeles.',2016, 128, 8.3, 258682, 151.06, 93)
( 'Mindhorn', 'A has-been actor best known for playing the title character in the 1980s detective series ""Mindhorn"" must work with the police when a serial killer says that he will only speak with Detective Mindhorn, whom he believes to be a real person.',2016, 89, 6.4, 2490, 0, 71 )
('The Lost City of Z','A true-life drama, centering on British explorer Col. Percival Fawcett, who disappeared while searching for a mysterious city in the Amazon in the 1920s.', 2016, 141, 7.1, 7188, 8.01,78 )
('Passengers','A spacecraft traveling to a distant colony planet and transporting thousands of people has a malfunction in its sleep chambers. As a result, two passengers are awakened 90 years early.', 2016, 116, 7, 192177, 100.01,41)
('Fantastic Beasts and Where to Find Them', 'The adventures of writer Newt Scamander in New Yorks secret community of witches and wizards seventy years before Harry Potter reads his book in school.', 2016,133,7.5,232072,234.02,66)
( 'Hidden Figures', 'The story of a team of female African-American mathematicians who served a vital role in NASA during the early years of the U.S. space program.', 2016,127,7.8,93103,169.27,74)
('Rogue One', '"The Rebel Alliance makes a risky move to steal the plans for the Death Star, setting up the epic saga to follow.', 2016,133,7.9,323118,532.17,65)
('Moana', 'In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an impetuous Chieftains daughters island, she answers the Oceans call to seek out the Demigod to set things right.',2016,107,7.7,118151,248.75,81)
('Colossal', '"Gloria is an out-of-work party girl forced to leave her life in New York City, and move back home. When reports surface that a giant creature is destroying Seoul, she gradually comes to the realization that she is somehow connected to this phenomenon.',2016,87,6.6,120259,368.31,61 )
('The Secret Life of Pets', 'The quiet life of a terrier named Max is upended when his owner takes in Duke, a stray whom Max instantly dislikes.', 2016,87,6.6,120259,368.31,61)
('Hacksaw Ridge', 'WWII American Army Medic Desmond T. Doss, who served during the Battle of Okinawa, refuses to kill people, and becomes the first man in American history to receive the Medal of Honor without firing a shot.',2016,139,8.2,211760,67.12,71 )
('Jason Bourne', 'The CIAs most dangerous former operative is drawn out of hiding to uncover more explosive truths about his past.', 2016,123,6.7,150823,162.16,58 )
('Lion', 'A five-year-old Indian boy gets lost on the streets of Calcutta, thousands of kilometers from home. He survives many challenges before being adopted by a couple in Australia. 25 years later, he sets out to find his lost family.',2016,118,8.1,102061,51.69,69)
('Arrival', 'When twelve mysterious spacecraft appear around the world, linguistics professor Louise Banks is tasked with interpreting the language of the apparent alien visitors.',2016,116,8,340798,100.5,81)
('Gold ', 'Kenny Wells, a prospector desperate for a lucky break, teams up with a similarly eager geologist and sets off on a journey to find gold in the uncharted jungle of Indonesia.',)
('Manchester by the Sea', 'A depressed uncle is asked to take care of his teenage nephew after the boy's father dies.',)
('Hounds of Love', 'A cold-blooded predatory couple while cruising the streets in search of their next victim, will stumble upon a 17-year-old high school girl, who will be sedated, abducted and chained in the strangers' guest room.',)
('Trolls', '',)
('Independance Day', '' )
('Paris Pieds Nus', '',)
('Bahubali', '',)
('Dead Awake', '',)
('Bad Moms', '',)
('Assassins Creed', '',)
('Why Him?', '',)
('Noctunrnal Animals', '',)
('X-Men', '',)
('Deadpool', '',)
('Resident Evil The Final Chapter', '',)
('Captain America: Cival War', '',)
('Intersteller', '',)
('Doctor Strange', '',)
('The Magnificent Seven', '',)



INSERT INTO movies.director_ref (first_name, middle_name, last_name)
VALUES
('James', NULL, 'Gunn'),
('Ridley', NULL, 'Scott'),
('M.', 'Night', 'Shyamalan'),
('Christophe', NULL, 'Lourdelet'),
('David', NULL, 'Ayer');
('Yimou', NULL, 'Zang'),
('Damien', NULL, 'Chazelle'),
('Sean', NULL, 'Foley'),
('James', NULL, 'Gray'),
('Morten', NULL, 'Tyldum'),
('David', NULL, 'Yates'),
('Theadore', NULL, 'Melfi'),
('Gareth', NULL, 'Edwards'),
('Ron', NULL, 'Clements'),
('Nacho', NULL, 'Vigalondo'),
('Chris', NULL, 'Renaud'),
('Mel', NULL, 'Gibson'),
('Paul', NULL, 'Greengrass'),
('Garth', NULL, 'Davis'),
('Denis', NULL, 'Villeneuve'),
('Stephen', NULL, 'Gaghan'),

INSERT INTO movies.genre_ref(genre)
VALUES
('Action'),
('Adventure')
('Animation'), 
('Biography'), 
('Comedy'), 
('Crime'),
('Drama'),
('Family'),
('Fantasy'),
('History'),
('Horror'),
('Mystery'),
('Sci-Fi'),
('Thriller'),
('Western'),
('Romance'),
('Sport'),
('Music'),
('War'),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),
('', '', ''),