import os
import shutil
import logging
import argparse 
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import configparser
import google.generativeai as genai
from pdfquery import PDFQuery
import PIL.Image

def find_topic(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    words = [word for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    word_counts = Counter(words)
    common_words = word_counts.most_common(5)
    return common_words[0]
  
GOOGLE_API_KEY= 'YOUR_API_KEY_HERE'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')

def load_config(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)
  return config

def get_pic_topic(pic):
  response = model.generate_content(["Give me a one word theme for this image", pic])
  return response.text


logger = logging.getLogger('organizer')


ch = logging.StreamHandler()


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter) 


logger.addHandler(ch)


CONFIG_FILE = 'config.ini'

def organize_files(root_folder, use_ai=False, dry_run=False):
  config = load_config(CONFIG_FILE)
  file_count = 0
  if use_ai:
    logger.info('Using AI for file organization')
    for folder, subs, files in tqdm(os.walk(root_folder), desc='Organizing'):
      for file in files:
        filename = file.split('.')[0]
        extension = file.split('.')[1]
        src = "C:/Users/MY PC/Downloads/"+file
        if file.endswith('.txt'):
          with open(os.path.join(folder, file), 'r') as f:
            text = f.read().join(' ')
            topic = find_topic(text)

            dest_folder = os.path.join(root_folder, topic)
            dest = os.path.join(dest_folder, file)
            if not os.path.exists(dest_folder):
              os.makedirs(dest_folder)
            if os.path.exists(dest):
              logger.warning(f'File {dest} already exists. Renaming file to avoid overwrite.')
              dest = os.path.join(dest_folder, f'{filename}_{datetime.now().strftime("%Y%m%d%H%M%S")}{extension}')
            if not dry_run:
              shutil.move(src, dest)
              f.close()
            else:
              logger.info(f'Dry run: {src} would be moved to {dest}')
              f.close()
        elif file.endswith('jpg') or file.endswith('png'):
            pic = os.path.join(folder, file)
            img = PIL.Image.open(pic)
            topic = get_pic_topic(img)
            dest_folder = os.path.join(root_folder, topic)
            dest = os.path.join(dest_folder, file)
            if not os.path.exists(dest_folder):
              os.makedirs(dest_folder)
            if os.path.exists(dest):
              logger.warning(f'File {dest} already exists. Renaming file to avoid overwrite.')
              dest = os.path.join(dest_folder, f'{filename}_{datetime.now().strftime("%Y%m%d%H%M%S")}{extension}')
            if not dry_run:
              shutil.move(src, dest)
            else:
              logger.info(f'Dry run: {src} would be moved to {dest}')
        elif file.endswith('.pdf'):
          mon_pdf = os.path.join(folder, file)
          pdf = PDFQuery(mon_pdf)
          pdf.load()
          text_elements = pdf.pq('LTTextLineHorizontal')
          text = [t.text for t in text_elements]
          topic = find_topic(text)
          dest_folder = os.path.join(root_folder, topic)
          dest = os.path.join(dest_folder, file)
          if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
          if os.path.exists(dest):
            logger.warning(f'File {dest} already exists. Renaming file to avoid overwrite.')
            dest = os.path.join(dest_folder, f'{filename}_{datetime.now().strftime("%Y%m%d%H%M%S")}{extension}')
          if not dry_run:
            shutil.move(src, dest)
          else:
            logger.info(f'Dry run: {src} would be moved to {dest}')
        else:
          try:
            file_count += 1
            src = os.path.join(folder, file)
            filename, extension = os.path.splitext(file)
            dest_folder = os.path.join(root_folder, config['folders'][extension]) 
            dest = os.path.join(dest_folder, file)
            if not os.path.exists(dest_folder):
              os.makedirs(dest_folder)
            if os.path.exists(dest):
              logger.warning(f'File {dest} already exists. Renaming file to avoid overwrite.')
              dest = os.path.join(dest_folder, f'{filename}_{datetime.now().strftime("%Y%m%d%H%M%S")}{extension}')
            if not dry_run:
              shutil.move(src, dest)
            else:
              logger.info(f'Dry run: {src} would be moved to {dest}')
          except Exception as e:
            logger.error(f'Error organizing file {src}: {str(e)}')
        
  else:
    logger.info('Using rules for file organization')
    for folder, subs, files in tqdm(os.walk(root_folder), desc='Organizing'):
    
      for file in files:
        filename = file.split('.')[0]
        extension = file.split('.')[1]
        src = "C:/Users/MY PC/Downloads/"+file
        try:
          file_count += 1
          src = os.path.join(folder, file)
          filename, extension = os.path.splitext(file)
          dest_folder = os.path.join(root_folder, config['folders'][extension]) 
          dest = os.path.join(dest_folder, file)
          if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
          if os.path.exists(dest):
            logger.warning(f'File {dest} already exists. Renaming file to avoid overwrite.')
            dest = os.path.join(dest_folder, f'{filename}_{datetime.now().strftime("%Y%m%d%H%M%S")}{extension}')
          if not dry_run:
            shutil.move(src, dest)
          else:
            logger.info(f'Dry run: {src} would be moved to {dest}')

        except Exception as e:
          logger.error(f'Error organizing file {src}: {str(e)}')

  
  logger.info(f'Total files organized: {file_count}') 

if __name__ == '__main__':

  
  parser = argparse.ArgumentParser()
  parser.add_argument('folder', help='Folder to organize')
  parser.add_argument('--use-ai', action='store_true', help='Use AI for file organization')
  parser.add_argument('--dry-run', action='store_true', help='Simulate file organization without moving files')
  parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help='Set the logging level')
  args = parser.parse_args()

  
  logger.setLevel(args.log_level)
  ch.setLevel(args.log_level)

  
  organize_files(args.folder, args.use_ai, args.dry_run)