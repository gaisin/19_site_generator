from jinja2 import Environment, FileSystemLoader
import markdown
import os
import json


def load_config(config_file):
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config_json = config_file.read()
        config_dict = json.loads(config_json)
    return config_dict


def load_markdown(source):
    with open('articles/{}'.format(source),
                    'r',
                    encoding='utf-8') as md_file:
            markdown_content = md_file.read()
    return markdown_content


def convert_markdown_to_html(markdown_content):
    html_content = markdown.markdown(markdown_content)
    return html_content


def save_to_html(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as html_page:
        html_page.write(content)


def render_article_html(template, content, title, static_path):
    return template.render(
                    md_content=content,
                    md_title=title,
                    static_path=static_path)


def render_index_html(template, topics, articles, static_path, title):
    return template.render(
                    topics=topics,
                    articles=articles,
                    static_path=static_path,
                    title=title)


if __name__ == '__main__':
    config_dict = load_config('config.json')

    env = Environment(loader=FileSystemLoader(searchpath='templates'))

    article_template = env.get_template('article_template.html')

    for article in config_dict['articles']:
        markdown_content = load_markdown(article['source'])
        article_html_content = convert_markdown_to_html(markdown_content)

        article_title = article['title']
        article_basename = os.path.basename(article['source'])
        article_name_without_extension = os.path.splitext(article_basename)[0]
        article['html_link'] = '{}.html'.format(article_name_without_extension)

        article_savepath = 'docs/articles/{}.html'\
                                .format(article_name_without_extension)

        article_content_to_save = render_article_html(
                                article_template,
                                article_html_content,
                                article_title,
                                '../static')

        save_to_html(article_savepath, article_content_to_save)

    # Creating index HTML page
    index_template = env.get_template('index_template.html')

    index_content_to_save = render_index_html(
                                index_template,
                                config_dict['topics'],
                                config_dict['articles'],
                                'static',
                                'Энциклопедия начинающего питониста')

    index_savepath = 'docs/index.html'

    save_to_html(index_savepath, index_content_to_save)
