from nltk.corpus import stopwords

data_root = '/home/gautham/work/kaggle/truly_native/data'
original_data_path = data_root + '/original'

train_classes_file = data_root + '/train.pickle'

all_word_count_file = data_root + '/all_word_count.pickle'
sponsored_word_count_file = data_root + '/sponsored_word_count.pickle'
organic_word_count_file = data_root + '/organic_word_count.pickle'
page_word_count_zip_file = data_root + '/page_word_count.zip'

html_zip = data_root + '/html.zip'
#html_cleaned_zip = data_root + '/html_cleaned.zip'
#html_cleaned_zip = data_root + '/html_cleaned2_no_text.zip'
html_cleaned_zip = data_root + '/html_cleaned3.zip'

html_config = data_root + '/html_config.pickle'
doc_mat = data_root + '/html_cleaned3_docmat.npz'

common_words = set(stopwords.words('english'))

max_word_len = 20
