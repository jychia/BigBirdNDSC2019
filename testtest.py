# Natural Language Processing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model.stochastic_gradient import SGDClassifier

def preprocess_data(titles, regex):
    ps = PorterStemmer()
    data = []
    for i in range(0, len(titles)):
        title = re.sub(regex, ' ', titles[i])
        title = title.lower()
        title = title.split()
        title = [ps.stem(word) for word in title if not word in set(stopwords.words('english'))]
        title = ' '.join(title)
        data.append(title)
        
    del titles
        
    return data

def vectorize_data(vectorizer, data):
    vectors = vectorizer.fit_transform(data).toarray()
    return vectors





# Importing the dataset
dataset = pd.read_csv('mobile_data_info_train_competition.csv', quoting = 3)

# Update stopwords database
nltk.download('stopwords')

classifier = RandomForestClassifier(n_estimators = 300, criterion = 'entropy', random_state = 0, max_depth=100)
#SGDClassifier(alpha=0.0001, penalty='elasticnet')

attr_name = 'Brand'
regex = '[^a-zA-Z0-9]'

# Some declaration and initialization
X = []
    
# Remove NaN entries from Benefits attribute
dataset_attr = dataset.dropna(subset=[attr_name])
    
# Cleaning the titles
X_title = preprocess_data(dataset_attr['title'].values, regex)
    
# Using Count Vectorizer as features
X = vectorize_data(CountVectorizer(max_features = 10000), X_title)

y = dataset_attr[attr_name].values
    
# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
X_title_train, X_title_test = train_test_split(X_title, test_size = 0.20, random_state = 0)
    
del X, y
    
classifier.fit(X_train, y_train)
    
# Predicting the Test set results
y_pred = classifier.predict(X_test)
    
# Calculate accuracy score
accuracy = accuracy_score(y_test, y_pred)
    
# Calculate F1 score
f1 = f1_score(y_test, y_pred, average='weighted')
    
y_train_pred = classifier.predict(X_train)
accuracy_train = accuracy_score(y_train, y_train_pred)
f1_train = f1_score(y_train, y_train_pred, average='weighted')
    
df = pd.DataFrame(data={'title': X_title_test, 'actual': y_test, 'pred': y_pred})
df_wrong = df[df.actual != df.pred]

cm = confusion_matrix(y_test, y_pred)



"""
acc_OS, f1_OS = train_predict_data(dataset, 'Operating System', classifier, '[^a-zA-Z]')
print("OS: acc=", acc_OS, ", f1=", f1_OS)

acc_Features, f1_Features, acc_Features_train, f1_Features_train, df_Features = train_predict_data(dataset, 'Features', classifier, '[^a-zA-Z0-9]')
print("Features: acc=", acc_Features, ", f1=", f1_Features)

acc_Network, f1_Network = train_predict_data(dataset, 'Network Connections', classifier, '[^a-zA-Z0-9]')
print("Network Connections: acc=", acc_Network, ", f1=", f1_Network)

acc_RAM, f1_RAM = train_predict_data(dataset, 'Memory RAM', classifier, '[^a-zA-Z0-9]')
print("Memory RAM: acc=", acc_RAM, ", f1=", f1_RAM)

acc_Brand, f1_Brand = train_predict_data(dataset, 'Brand', classifier, '[^a-zA-Z]')
print("Brand: acc=", acc_Brand, ", f1=", f1_Brand)

acc_Warranty, f1_Warranty = train_predict_data(dataset, 'Warranty Period', classifier, '[^a-zA-Z0-9]')
print("Warranty Period: acc=", acc_Warranty, ", f1=", f1_Warranty)

acc_Storage, f1_Storage = train_predict_data(dataset, 'Storage Capacity', classifier, '[^a-zA-Z0-9]')
print("Storage Capacity: acc=", acc_Storage, ", f1=", f1_Storage)

acc_Color, f1_Color = train_predict_data(dataset, 'Color Family', classifier, '[^a-zA-Z]')
print("Color Family: acc=", acc_Color, ", f1=", f1_Color)

acc_Model, f1_Model = train_predict_data(dataset, 'Phone Model', classifier, '[^a-zA-Z0-9]')
print("Phone Model: acc=", acc_Model, ", f1=", f1_Model)

acc_Camera, f1_Camera = train_predict_data(dataset, 'Camera', classifier, '[^a-zA-Z0-9]')
print("Camera: acc=", acc_Camera, ", f1=", f1_Camera)

acc_Size, f1_Size = train_predict_data(dataset, 'Phone Screen Size', classifier, '[^a-zA-Z0-9]')
print("Phone Screen Size: acc=", acc_Size, ", f1=", f1_Size)

"""