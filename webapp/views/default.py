import colander
import deform.widget

from docutils.core import publish_parts
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.view import view_config
import re

from .. import models
from datetime import datetime
from sqlalchemy import or_

_global_tag_search = None

class WikiPage(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
    )

wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='view_wiki')
def view_wiki(request):
    next_url = request.route_url('list_pages')
    return HTTPSeeOther(location=next_url)

@view_config(route_name='list_pages', renderer='webapp:templates/list_pages.jinja2', permission='view')
def list_pages(request):
    tag_search = request.params.get('tag_search')
    alert = False
    global _global_tag_search

    show_all = request.params.get('showAll') == 'true'
    if show_all:
        _global_tag_search = None
        tag_search = None

    if tag_search:
        _global_tag_search = tag_search
        pages = request.dbsession.query(models.Page).filter(
            or_(*[models.Page.tags.ilike(f'%{tag.strip()}%') for tag in _global_tag_search.split(',') if tag])
        ).all()
        if not pages:
            _global_tag_search = None
            alert = True
    else:
        if _global_tag_search:
            pages = request.dbsession.query(models.Page).filter(
                or_(*[models.Page.tags.ilike(f'%{tag.strip()}%') for tag in _global_tag_search.split(',') if tag])
            ).all()
            if not pages:
                _global_tag_search = None
                alert = True
        else:
            pages = request.dbsession.query(models.Page).all()

    if(alert == True):
        pages = request.dbsession.query(models.Page).all()

    is_editor = False
    if request.identity is not None:
        if request.identity.role == 'editor':
            is_editor = True
    return {'pages': pages, 'is_editor': is_editor, 'alert': alert, 'global_tag_search': _global_tag_search}
 
@view_config(route_name='view_page', renderer='webapp:templates/view.jinja2', permission='view')
def view_page(request):
    userId = 1
    userName = 'Anonymous'

    is_editor = False
    if request.identity is not None:
        userName = request.identity.name
        if request.identity.role == 'editor':
            is_editor = True

    page = request.context.page

    if request.method == 'GET':
        try:
            comment_content = request.GET.get('comment', '')          
            if comment_content:
                new_comment = models.Comment(
                content=comment_content,
                user_id=userId,
                user_name=userName,
                page=page
                )

                request.dbsession.add(new_comment)
                return HTTPSeeOther(request.route_url('view_page', pagename=page.name))
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
   
    content = publish_parts(page.data, writer_name='html')['html_body']
    edit_url = request.route_url('edit_page', pagename=page.name)
    return dict(page=page, content=content, edit_url=edit_url, is_editor = is_editor, tags=page.tags)

@view_config(route_name='edit_page', renderer='webapp:templates/edit.jinja2', permission='edit')
def edit_page(request):
    page = request.context.page
    if request.method == 'POST':
        page.name = request.params['name']
        page.tags = request.params['tags']
        page.publication_date = datetime.utcnow()
        page.data = request.params.get('body', '') 
        next_url = request.route_url('view_page', pagename=page.name)
        return HTTPSeeOther(location=next_url)
    return dict(
        pagename=page.name,
        tags=page.tags,
        publication_date=page.publication_date.strftime('%Y-%m-%d %H:%M'),
        pagedata=page.data,
        save_url=request.route_url('edit_page', pagename=page.name),
    )

@view_config(route_name='add_page', renderer='webapp:templates/edit.jinja2',
             permission='create')
def add_page(request):
    pagename = request.context.pagename
    if request.method == 'POST':
        body = request.params['body']
        tags = request.params['tags']
        name = request.params['name']
        publication_date = datetime.utcnow()
        page = models.Page(name=name, data=body, tags=tags, publication_date=publication_date)
        page.creator = request.identity
        request.dbsession.add(page)
        next_url = request.route_url('view_page', pagename=name)
        return HTTPSeeOther(location=next_url)
    save_url = request.route_url('add_page', pagename=pagename)
    return dict(pagename=pagename, pagedata='', save_url=save_url)

