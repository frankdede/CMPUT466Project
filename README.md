T12 - Sentiment Analysis on Movie Reviews
===============
Team members:
Yuwei Duan - yuwei@ualberta.ca 
Guanqi Huang - guanqi@ualberta.ca 
Chongyang Ye - cye2@ualberta.ca
Tianyi Wu - twu5@ualberta.ca

===============
Abstract:

Our task is to label phrases from the Rotten Tomatoes movie review dataset on a scale of five values: 0 ­ negative, 1 ­ somewhat negative, 2 ­ neutral, 3 ­ somewhat positive, 4 ­ positive. The challenges that we may encounter are the variation in human language expression such as sarcasm, terseness etc.
We found our topic from Kaggle.com. Kaggle.com provides both the testing data and the training data.
https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews
					
===============
Data Structure:

The training dataset contains four features: PharseId,SentenceId,Phrase and Sentiment. There are 8544 sentences (meaningful and human readable english sentences) in total, some of the sentences are splitted into short phrases. Therefore, those short phrases are the subset of the same sentence. Each phrase is associated with a sentiment label, those labels are represented by integers ranging from 0 to 4.
					
===============
Theoretical paper links:

Supervised Machine Learning:A Review of Classification Techniques:
http://www.informatica.si/PDF/31-3/11_Kotsiantis%20-%20Supervised%20Machine%20Learning%20-%20A%20Review%20of...pdf
					
Text Categorization using Feature Projections:
http://www.aclweb.org/anthology/C02-1074

Application of k-nearest neighbor on feature projections classifier to text categorization:
http://www.google.ca/books?hl=zh-CN&lr=&id=ClU2XG64UOIC&oi=fnd&pg=PA135&dq=Application+of+k-nearest+neighbor+on+feature+projections+classifier+to+text+categorization&ots=RYmZC-Mo31&sig=NsEansixZ_xx7XPnYWWAXqnehtI&redir_esc=y#v=onepage&q=Application%20of%20k-nearest%20neighbor%20on%20feature%20projections%20classifier%20to%20text%20categorization&f=false
						

Algorithm Implementation paper links:
scikit tutorial - python machine learning libraries 
http://scikit-learn.org/stable/documentation.html

================================
Licence:
All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

================================
REFERENCE:
Default English stopwords list: 
http://www.ranks.nl/stopwords
