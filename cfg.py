from nltk.corpus import stopwords

data_root = '/home/gautham/work/kaggle/truly_native/data'
original_data_path = data_root + '/original'

html_zip = data_root + '/html.zip'
html_cleaned_zip = data_root + '/html_cleaned.zip'

common_words = set(stopwords.words('english'))

max_word_len = 20
