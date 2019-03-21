
# Jillian James, jiljames at reed dot edu
# Program for reading tags to create matrix file for training algorithm


import os
import glob
import json
import csv
import pandas as pd

path = '/Users/jillianjames/systemsproject/fulltext'
sorted_tags = ['analysis', 'bigscale', 'continuing', 'data', 'experience','experiment', 'negative', 'open', 'position', 'positive', 'preliminary', 'reproduction', 'simulation', 'survey', 'system'] 


###### FOR READING TAGS AND GENERATING TAG_FEATURES.CSV #######

def getConfAndPaper(filepath):
	confname = ""
	paper = filepath[-11:-4]
	place = -12
	letter = filepath[place]
	while letter != "/":
		confname = letter + confname
		paper = letter + paper
		place -= 1
		letter = filepath[place]
	return confname, paper


def fixedToInt(string3):
	i = 2
	total = 0
	for num in string3:
		total += int(num)*(10**i)
		i -= 1
	return total


def read_tags(confname, paper):
	papernum = fixedToInt(paper[-3::]) 
	with open("conf/"+confname+".json") as f:
		data = json.load(f)
		try:
			return data['papers'][papernum-1]['content_tags']['manual']
		except KeyError:
			return
		f.close()

def generate_row(paper, manual, sorted_tags):
	manual.sort()
	row = {"Name": paper}
	for tag in sorted_tags:
		row["tag_id_"+tag] = 0
	for tag in manual:
		if tag in sorted_tags:
			row["tag_id_"+tag]+=1
		else:
			print("This paper has incorrect tags: "+paper)
	return row


def make_tag_features():
	# Make column header:
	column_labels = sorted_tags[:]
	for i in range(len(column_labels)):
		column_labels[i] = "tag_id_"+column_labels[i]
	# Create writer:
	with open("tag_features.csv", 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = ["Name"]+column_labels)
		writer.writeheader()

		for filepath in glob.glob(path+'/*.txt'):
			confname, paper = getConfAndPaper(filepath)
			manual = read_tags(confname,paper)
			if manual != None:
				row = generate_row(paper,manual,sorted_tags)
				writer.writerow(row)
			
		csvfile.close()
	print("Assigned tags read. Tag columns generated.")
	return



####### SIMPLE FUNCTION TO COUNT OCCURENCES/PERCENTAGE OF TAGS ########

def count_tags():
	with open("tag_features.csv", 'r') as tagcsv:
		tf = pd.read_csv(tagcsv)
		tagcsv.close()
	for tag in sorted_tags:
		tag_column = tf[tag.lower()]
		i = 0
		for instance in tag_column:
			if instance == 1:
				i += 1
		print(tag+" counts: "+str(i))
		print("Percentage: "+str((i/len(tag_column))*100))
		print("------------------")
	print("Total Papers: "+str(len(tag_column)))
	return



##### FOR CREATING ____matrix.csv FILE ###########


# def make_tag_matrix(tag, lemmatized = True):
# 	with open("tag_features.csv", 'r') as tagcsv:
# 		tf = pd.read_csv(tagcsv)
# 		tagcsv.close()
	
# 	#Pick wf as either regular or lemmatized token files
# 	#based on parameters.

# 	if lemmatized == False:
# 		with open("tokens.csv", "r") as tokencsv:
# 			wf = pd.read_csv(tokencsv)
# 			tokencsv.close()
# 	else:
# 		with open("lemmatized_tokens.csv", "r") as tokencsv:
# 			wf = pd.read_csv(tokencsv)
# 			tokencsv.close()

# 	#save tagged paper names and relevant tag column
# 	tagged_papers = tf["Name"]
# 	tag_column = tf["tag_id_"+tag.lower()]

# 	#save all paper names, all words, and all counts
# 	papers = wf["doc_id"]
# 	words = wf["word"]
# 	count = wf["n"]

# 	#Add the "Name" and tag columns to column labels
# 	column_labels = words.drop_duplicates()
# 	column_labels = pd.concat([pd.Series(["Name"]), column_labels])
# 	column_labels = pd.concat([column_labels, pd.Series([tag])])

# 	#Write the matrix
# 	with open(tag+"_matrix.csv", "w") as csvfile:
# 		writer = csv.DictWriter(csvfile, fieldnames = column_labels)
# 		writer.writeheader()

# 		baserow = {}
# 		#Initialize each row to contain all zeroes
# 		for label in column_labels:
# 			baserow[label] = 0
# 		j = 0

# 		#If a paper is tagged, make a row of it with
# 		# all its word counts and write to matrix
# 		for tpaper in tagged_papers:
# 			row = baserow
# 			row["Name"] = tpaper
# 			i = 0
# 			for paper in papers:
# 				if paper == tpaper:
# 					row[words[i]] = count[i]
# 				i+=1
# 			####FOUND IT!!!!####	
# 			row["tag_id_"+tag.lower()] = tag_column[j]
# 			j+=1
# 			writer.writerow(row)

# 		csvfile.close()
# 	return



def make_tag_matrix(tag):
	with open("tag_features.csv", 'r') as tagcsv:
		tf = pd.read_csv(tagcsv)
		tagcsv.close()
	
	#Pick wf as either regular or lemmatized token files
	#based on parameters.
	#save tagged paper names and relevant tag column
	tagged_papers = tf["Name"]
	tag_column = tf["tag_id_"+tag.lower()]

	# with open("lemmatized_tokens.csv", "r") as tokencsv:
	# 		wf = pd.read_csv(tokencsv)
	# 		tokencsv.close()

	# with open("bigrams.csv", 'r') as bigramcsv:
	# 		bf = pd.read_csv(bigramcsv)
	# 		bigramcsv.close()

	with open("all-terms.csv", 'r') as alltermscsv:
			allf = pd.read_csv(alltermscsv)
			alltermscsv.close()

	#just stack the words and bigrams dataframes together
	#!!!!!!comment out to remove error!!!!!!!
	# wbf = wf.append(bf)
	#save all paper names, all words, and all counts
	#!!!!!!change to wf or bf to remove error!!!!!!

	papers = allf["doc_id"]
	words = allf["term"]
	# df['column'] = df['column'].astype('|S')
	count = allf["n"]

	print("attatched matrices")


	#Add the "Name" and tag columns to column labels
	column_labels = words.drop_duplicates()
	column_labels = pd.concat([pd.Series(["doc_id_"]), column_labels])
	column_labels = pd.concat([column_labels, pd.Series(["tag_id_"+tag.lower()])])

	#Write the matrix
	with open(tag+"_matrix.csv", "w") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = column_labels)
		writer.writeheader()

		baserow = {}
		#Initialize each row to contain all zeroes
		for label in column_labels:
			baserow[label] = 0
		j = 0

		#If a paper is tagged, make a row of it with
		# all its word counts and write to matrix
		for tpaper in tagged_papers:
			row = baserow
			row["doc_id_"] = tpaper
			i = 0
			for paper in papers:
				if paper == tpaper:
					row[words.iloc[i]] = count.iloc[i]
				i+=1
			####FOUND IT!!!!####	
			row["tag_id_"+tag.lower()] = tag_column[j]
			j+=1
			writer.writerow(row)

		csvfile.close()
	print("Tag matrix completed. Ready for training.")
	return



def main():
	make_tag_features()
	make_tag_matrix("analysis")


