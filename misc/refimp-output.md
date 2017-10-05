# Reference implementation output on VM

## ssh command and password (cs6111)

```bash
$ ssh guest-user@35.196.105.51
no such identity: /home/rasbar/.ssh/google-compute_engine: No such file or directory
guest-user@35.196.105.51's password: 
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 4.4.0-93-generic x86_64)
```

## Implemenation run 1: query = "per se"

```bash

guest-user@cs6111:~$ /home/paparrizos/run "AIzaSyAlKLHe1eAmug6XeTlQ1DxzOsPI4zax7Ms" "006096712590953604068:qoxtr78cjow" 0.9 "per se"
Parameters:
Client key  = AIzaSyAlKLHe1eAmug6XeTlQ1DxzOsPI4zax7Ms
Engine key  = 006096712590953604068:qoxtr78cjow
Query       = per se
Precision   = 0.9
Google Search Results:
======================
Result 1
[
 URL: https://www.thomaskeller.com/perseny
 Title: Per Se | Thomas Keller Restaurant Group
 Summary: Per Se entrance. center. Macadamia nut dipped in chocolate. left. Mini meat filled 
pastries. right. Per Se Salon. center. Fish and vegetables. right. Oysters and ...
]

Relevant (Y/N)?y
Result 2
[
 URL: http://www.dictionary.com/browse/per-se
 Title: Per se | Define Per se at Dictionary.com
 Summary: Per se definition, by, of, for, or in itself; intrinsically: This candidate is not a pacifist 
per se, but he is in favor of peaceful solutions when practicable. See more.
]

Relevant (Y/N)?n
Result 3
[
 URL: https://www.merriam-webster.com/dictionary/perse
 Title: Perse | Definition of Perse by Merriam-Webster
 Summary: Define perse: of a dark grayish blue resembling indigo — perse in a sentence.
]

Relevant (Y/N)?n
Result 4
[
 URL: https://en.wiktionary.org/wiki/per_se
 Title: per se - Wiktionary
 Summary: Borrowed from Latin per se (“by itself”), from per (“by, through”) and se (“itself, 
himself, ... Well, that's not correct per se, but the situation is something like that.
]

Relevant (Y/N)?n
Result 5
[
 URL: https://en.wikipedia.org/wiki/Per_se
 Title: Per se - Wikipedia
 Summary: Per se may refer to: per se (Latin), a Latin phrase meaning "by itself" or "in itself". 
Illegal per se, the legal usage in criminal and anti-trust law; Negligence per se, ...
]

Relevant (Y/N)?n
Result 6
[
 URL: https://www.yelp.com/biz/per-se-new-york
 Title: Per Se - 3875 Photos & 1287 Reviews - French - 10 Columbus Cir ...
 Summary: 1287 reviews of Per Se "Per Se is the best of the best. I've had the pleasure of 
dining at many of the worlds "Best Restaurants" and Per Se is obvious why they'
re ...
]

Relevant (Y/N)?y
Result 7
[
 URL: https://www.nytimes.com/2016/01/13/dining/pete-wells-per-se-review.html
 Title: At Thomas Keller's Per Se, Slips and Stumbles - The New York Times
 Summary: Jan 12, 2016 ... Such is Per Se's mystique that I briefly wondered if the failure to bring her a new 
napkin could have been intentional. The restaurant's identity, to ...
]

Relevant (Y/N)?y
Result 8
[
 URL: https://www.vocabulary.com/dictionary/per%20se
 Title: per se - Dictionary Definition : Vocabulary.com
 Summary: Per se is the phrase to use when you want to refer to a particular thing on its own. 
It is not this Latin phrase, per se, that is important, but rather the concept it ...
]

Relevant (Y/N)?n
Result 9
[
 URL: https://en.wikipedia.org/wiki/Per_Se_(restaurant)
 Title: Per Se (restaurant) - Wikipedia
 Summary: Per Se is a New American and French restaurant located on the fourth floor of the 
Time Warner Center at 10 Columbus Circle in Manhattan in New York City, ...
]

Relevant (Y/N)?y
Result 10
[
 URL: https://www.opentable.com/per-se-reservations-new-york
 Title: Per Se reservations in New York, NY | OpenTable
 Summary: Make a restaurant reservation at Per Se in New York, NY. Select date, time, and 
party size to find a table.
]

Relevant (Y/N)?y
======================
FEEDBACK SUMMARY
Query per se
Precision 0.5
Still below the desired precision of 0.9
Indexing results ....
Indexing results ....
Augmenting by  restaurant york
Parameters:
Client key  = AIzaSyAlKLHe1eAmug6XeTlQ1DxzOsPI4zax7Ms
Engine key  = 006096712590953604068:qoxtr78cjow
Query       = per se restaurant york
Precision   = 0.9
Google Search Results:
======================

Result 1
[
 URL: https://www.thomaskeller.com/perseny
 Title: Per Se | Thomas Keller Restaurant Group
 Summary: Macadamia nut dipped in chocolate. left. Mini meat filled pastries. right. Per Se 
Salon. center. Fish and vegetables. right. Oysters and Caviar; resting on tapioca ...
]

Relevant (Y/N)?y
Result 2
[
 URL: https://www.nytimes.com/2016/01/13/dining/pete-wells-per-se-review.html
 Title: At Thomas Keller's Per Se, Slips and Stumbles - The New York Times
 Summary: Jan 12, 2016 ... The name Per Se, after all, was chosen to suggest that New York would not 
simply reflect California's glory; this would be a landmark restaurant ...
]

Relevant (Y/N)?y
Result 3
[
 URL: https://www.thomaskeller.com/new-york-new-york/per-se/restaurant
 Title: Per Se
 Summary: Restaurant. Opened in 2004, Per Se is Thomas Keller's acclaimed New York 
interpretation of The French Laundry in the Time Warner Center at Columbus 
Circle ...
]

Relevant (Y/N)?y
Result 4
[
 URL: https://www.opentable.com/per-se
 Title: Per Se Restaurant - New York, NY | OpenTable
 Summary: Book now at Per Se in New York, explore menu, see photos and read 1959 
reviews: "Marvelous!!!! Amazing food, great service... all that you can imagine and
 ...
]

Relevant (Y/N)?y
Result 5
[
 URL: https://www.thomaskeller.com/new-york-new-york/per-se/todays-menus
 Title: Per Se
 Summary: Daily Menus Two tasting menus are offered daily: a nine-course chef's tasting 
menu as well as a nine-course vegetable tasting menu. No single ingredient is ...
]

Relevant (Y/N)?y
Result 6
[
 URL: https://en.wikipedia.org/wiki/Per_Se_(restaurant)
 Title: Per Se (restaurant) - Wikipedia
 Summary: Per Se is a New American and French restaurant located on the fourth floor of the 
Time Warner Center at 10 Columbus Circle in Manhattan in New York City, ...
]

Relevant (Y/N)?y
Result 7
[
 URL: http://www.esquire.com/food-drink/restaurants/news/a41981/per-se-new-york-times-chef-reactions/
 Title: Why That Per Se Review May Change Fine Dining Forever
 Summary: Feb 10, 2016 ... Even when it opened in 2004, Per Se recalled an older school of luxury. New 
York restaurants have been skewing casual since the early 2000s ...
]

Relevant (Y/N)?y
Result 8
[
 URL: http://www.townandcountrymag.com/leisure/arts-and-culture/a7685/thomas-keller-per-se-new-york-times-review/
 Title: Thomas Keller Responds to New York Times Review of Per Se ...
 Summary: Sep 8, 2016 ... But on January 12 the New York Times had knocked Per Se, his seemingly 
untouchable restaurant on Columbus Circle in Manhattan, down ...
]

Relevant (Y/N)?y
Result 9
[
 URL: https://ny.eater.com/2016/1/28/10858508/thomas-keller-per-se-response
 Title: Keller Responds to Per Se Review: 'We Are Sorry We Let You Down ...
 Summary: Jan 28, 2016 ... The fact that The New York Times restaurant critic Pete Wells' dining experiences 
at Per Se did not live up to his expectations and to ours is ...
]

Relevant (Y/N)?y
Result 10
[
 URL: https://www.viamichelin.com/web/Restaurant/New_York-10019-Per_Se-69452-41102
 Title: Per Se - Manhattan : a Michelin Guide restaurant
 Summary: Per Se: Michelin Guide review, users review, type of cuisine, opening times, meal 
... Per Se. MICHELIN Guide 2017. 10 Columbus Circle, New York 10019.
]

Relevant (Y/N)?y
======================
FEEDBACK SUMMARY
Query per se restaurant york
Precision 1.0
Desired precision reached, done
guest-user@cs6111:~$ 
```
