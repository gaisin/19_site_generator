from jinja2 import Environment, FileSystemLoader
import markdown
import os
import json

# At first parsing config.json
with open('config.json', 'r', encoding='utf-8') as config_file:
    config_json = config_file.read()
    config_dict = json.loads(config_json)

# Creating articles HTML pages
env = Environment(loader=FileSystemLoader(searchpath='templates'))

article_template = env.get_template('article_template.html')

for article in config_dict['articles']:
    with open('articles/{}'.format(article['source']), 
                'r', 
                encoding='utf-8') as md_file:
        markdown_content = md_file.read()

    article_content = markdown.markdown(markdown_content)
    article_title = article['title']
    article_basename = os.path.basename(article['source'])
    article_name_without_extension = os.path.splitext(article_basename)[0]
    article['html_link'] = '{}.html'.format(article_name_without_extension)

    with open('docs/articles/{}.html'.format(article_name_without_extension), 
                'w', 
                encoding='utf-8') as html_page:
        html_page.write(article_template.render(
                        md_content=article_content,
                        md_title=article_title,
                        static_path = '../static',
                        title = article_title))

# Creating index HTML page
index_template = env.get_template('index_template.html')

with open('docs/index.html', 'w', encoding='utf-8') as index:
    index.write(index_template.render(
                                topics = config_dict['topics'], 
                                articles = config_dict['articles'], 
                                static_path = 'static',
                                title = 'Энциклопедия начинающего питониста'))

# Доделать:
# выложить на github pages
# попробовать сделать livereload