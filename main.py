import os
from pdf_to_text import pdfparser
import re
from tqdm import trange
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import pandas as pd
import numpy as np
from k_cluster import k_means
import platform


def folder_reader(path):
	files = os.listdir(path)
	files_pdf = [i for i in files if i.endswith('.pdf')]
	return files_pdf

def input_configs():

	path = input("Enter path to pdf's folder:\t")
	print()
	print("We can analyse the whole document in which case just enter 0 for first page and -1 for last page\n")
	f_pgs = int(input("Enter first page from which each document must be analysed:\t"))
	l_pgs = int(input("Enter last page till which each document must be analysed:\t"))
	print()
	path_o = input("Enter path to text saving folder if you don't then just leave it blank:\t")
	print()
	vectors_path = input("Enter path to vector table:\t")
	print()
	n_clusters = int(input("Enter number of final classes:\t"))


	return path, f_pgs, l_pgs, path_o, vectors_path, n_clusters


def folder_to_txt(path, f_pgs, l_pgs, path_o):
	
	documents = folder_reader(path)
	all_data = []
	for doc in trange(len(documents)):
		data = pdfparser(path+'/'+documents[doc], f_pgs, l_pgs)
		all_data.append(data)

	return all_data, documents
	
def save_txt(path_o, all_data, documents):
	if path_o.strip() == '':
		return 0
	else:
		for doc, data in zip(documents, all_data):
			file = open(path_o+'/'+doc[:-3]+'txt', 'w')
			data_raw = str(data.encode("ascii", 'ignore'))[2:]
			data_list = data_raw.split('\\n')
			data_list = [i+'\n' for i in data_list]
			file.writelines(data_list)
			file.close()

def only_text(all_data):
	all_data_txt = []
	
	for data in all_data:
		data_i = " ".join(re.findall(r"(?i)\b[a-z]+\b", data))
		all_data_txt.append(data_i)
	return all_data_txt

def tfidf_vect(all_data, vectors_path):

	stopwords_eng = stopwords.words('english') + ['\n']
	vectorizer = TfidfVectorizer(stop_words=stopwords_eng)
	vectors = vectorizer.fit_transform(all_data)
	feature_names = vectorizer.get_feature_names()
	dense = vectors.todense()
	denselist = dense.tolist()
	df = pd.DataFrame(denselist, columns=feature_names)
	df.to_csv(vectors_path)

	return feature_names, denselist

def collector(path, labels, documents):
	all_classes = {}
	for i in range(max(labels)+1):
		all_classes.update({i: []})
		if platform.system() == 'Windows':
			os.system('mkdir '+path.replace('/', '\\')+'\\classified\\'+str(i))
		else:
			os.system('mkdir '+path+'\\classified\\'+str(i))
	for label, doc in zip(labels, documents):
		all_classes[label].append(doc)

	os_type = platform.system()
	if os_type == 'Windows':
		copy = 'copy'
	else:
		copy = 'cp'
	for class_n, files in all_classes.items():
		for file in files:
			f_path = copy+' '+path+'/"'+file+'" '+path+'/classified/'+str(class_n)+'/"'+file+'"'
			if os_type == 'Windows':
				f_path = f_path.replace('/', '\\')
			os.system(f_path)




def main():
	nltk.download('stopwords')
	try:
		os.system('cls')
	except:
		os.system('clear')
	path, f_pgs, l_pgs, path_o, vectors_path, n_clusters = input_configs()
	all_data, documents = folder_to_txt(path, f_pgs, l_pgs, path_o)
	save_txt(path_o, all_data, documents)
	all_data = only_text(all_data)
	feature_names, denselist = tfidf_vect(all_data, vectors_path)
	labels = k_means(denselist, n_clusters)
	collector(path, labels, documents)

	
main()