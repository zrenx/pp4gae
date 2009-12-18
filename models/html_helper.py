import re
from gluon.contrib.gql import GQLDB

def get_post_author(author_id):
    user = db(db.users.id==author_id).select()[0]
    return XML(db(db.users.id == author_id).select()[0].alias)

def get_comment_count(post_id):
    com_count=len(db(db.comments.post_id==post_id).select(db.comments.ALL))
    if com_count == 0:
        com_text="No Comments &raquo;"
    elif com_count == 1:
        com_text="1 Comment &raquo;"
    else:
        com_text="%s Comments &raquo;" % com_count
    pass
    com_link = "<a href='%(url)s'>%(text)s</a>" % {'url':URL(r=request,f='post/%d#comments' % post_id), 'text':com_text}
    return XML(com_link)

def get_post_cats(post_id):
    posts=db(db.posts.id == post_id).select(db.posts.ALL)
    cats=db(db.categories.id == posts[0].post_category).select(db.categories.ALL)#[0]
    items=[]
    for cat in cats:
        item="<a href='%(url)s'>%(name)s</a>" % {'url':URL(r=request,f='category/%s' % cat.category_name), 'name':cat.category_name}
        items.append(item)
    pass
    cat_list=", ".join(items)
    return XML(cat_list)

# for the customized password update form
def form_factory(*a): return SQLFORM(GQLDB().define_table(*a))


def hyper_text(text):
    hyper = re.sub('\n','<br/>',text)
    return XML(hyper)

def url_text(text):
    if re.match(r'^[(http://)|(ftp://)|(https://)].+', text):
        return text
    else:
        return 'http://'+text
    
def get_file_type(text):
    images = ['image/jpeg','image/gif','image/png']
    if re.match("image/.+", str(text)):
        return 'image'
    else:
        return 'file'


def get_file_name(text):
    import base64
    encoded_name = text.split('.')[3]
    return base64.b16decode(encoded_name.upper()).decode('utf_8')