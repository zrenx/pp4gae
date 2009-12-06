#from gluon.fileutils import check_credentials
#session.authorized=check_credentials(request)

bloginfo = db().select(db.blog_info.ALL)[0]

response.name = bloginfo.name if bloginfo else "PyPress For GAE"
response.title = bloginfo.title if bloginfo else "pp4gae - a web2py powered weblog based on GAE"
response.keywords = bloginfo.keywords if bloginfo else "pypress4gae, pp4gae, GAE, web2py, Gluon, Python, Web, PyPress"
response.description = bloginfo.description if bloginfo else "Just another pypress4gae weblog"

# This dynamically adds the pages to the menu
pages = db(db.posts.post_type == 'page').select(db.posts.ALL)
items = []
for page in pages:
    #item = [page.post_title, False, '/%(app)s/default/page/%(id)s' % {'app':request.application, 'id':page.id}]
    item = [page.post_title, False, URL(r=request,f='page/%d' % page.id)]
    items.append(item)
response.menu = items

# This returns all the categories and their post count
cats = db().select(db.categories.ALL)
items = []
for cat in cats:
    count = len(db(
                   (db.posts.post_type == 'post') & 
                   (db.posts.post_category == cat.id)
                   ).select(db.posts.ALL))
    if count > 0:
        #item = [cat.category_name, count, '/%(app)s/default/category/%(name)s' % {'app':request.application, 'name':cat.category_name}]
        item = [cat.category_name, count, URL(r=request,f='category/%s' % cat.category_name)]
        items.append(item)
response.categories = items

# This returns all the links
links = db().select(db.links.ALL)
items = []
for link in links:
    item = [link.link_title, link.link_url, link.id]
    items.append(item)
response.links = items

# This returns latest 5 posts
last_posts = db(db.posts.post_type == 'post').select(db.posts.ALL, orderby=~db.posts.post_time|~db.posts.post_title, limitby=(0,5))
items = []
for post in last_posts:
    #item = [post.post_title, post.post_time, '/%(app)s/default/post/%(id)s' % {'app':request.application, 'id':post.id}]
    item = [post.post_title, post.post_time, URL(r = request, f = 'post/%d' % post.id)]
    items.append(item)
response.last_posts = items


# The main page
# Shows the first 10 posts    
def index():
    posts = db(db.posts.post_type == 'post').select(db.posts.ALL, orderby=~db.posts.post_time|~db.posts.post_title)
    #posts = db(db.posts.post_type == 'post').select(db.posts.ALL, orderby=db.posts.post_time)
    return dict(posts = posts)

# The post page
# Shows the entire post, the comments, and the comment form
def post():
    #try: 
    post_id = int(request.args[0])
    posts = db(db.posts.id == post_id).select()
    if not posts:
        redirect(URL(r = request,f = 'index'))
    post = posts[0]
    comments = db(db.comments.post_id == post_id).select(db.comments.ALL)
    comment_count = len(db(db.comments.post_id == post_id).select(db.comments.ALL))
    db.comments.post_id.default = post_id

    comment_form = SQLFORM(db.comments, fields = ['comment_author', 'comment_author_email', 'comment_author_website', 'comment_text'], labels = comment_labels)
    if comment_form.accepts(request.vars, session):
        session.flash = "Comment added."
        redirect(URL(r = request,f = 'post/%d' % post_id))
        
    return dict(post = post, comments = comments, comment_form = comment_form, comment_count = comment_count)
    #except: 
    #    redirect(URL(r = request,f = 'index'))

# The page page
# Shows the entire page. Does not show comments or the comment form
def page():
    try: 
        post_id = int(request.args[0])
        post = db(db.posts.id == post_id).select()[0]
        return dict(post = post)
    except: 
        redirect(URL(r = request,f = 'index'))

# The category page
# Shows all the posts in the requested category
def category():
    try:
        cat_name = request.args[0]
        #print 'start select db for category posts'
        cat_id = db(db.categories.category_name == cat_name).select()[0].id
        posts = db(
                   (db.posts.post_type == 'post') &
                   (db.posts.post_category == cat_id)
                   ).select(db.posts.ALL, orderby=~db.posts.post_time)
        #print posts
        response.sidebar_note = "You are currently browsing the archives for the %s category." % cat_name
        return dict(posts = posts)
    except:
        redirect(URL(r = request,f = 'index'))

def add():
    if not session.authorized:
        redirect(URL(r=request,f='index'))
        
    try:
        area = request.args[0]

        if area == "post":
            db.posts.post_type.default = 'post'
            db.posts.post_author.default = session.authorized
            page_form = SQLFORM(db.posts, fields = ['post_title', 'post_text', 'post_category'], labels = post_labels)
            page_title = "Add Post"
            
            if page_form.accepts(request.vars, session):
                session.flash = "Post added."
                redirect(URL(r = request,f = 'index'))
        
        elif area == "page":
            db.posts.post_type.default = 'page'
            db.posts.post_author.default = session.authorized
            page_form = SQLFORM(db.posts, fields = ['post_title', 'post_text'], labels = post_labels)
            page_title = "Add Page"
            
            if page_form.accepts(request.vars, session):
                session.flash = "Page added."
                redirect(URL(r = request,f = 'index'))
               
        elif area == "category":
            page_form = SQLFORM(db.categories, fields = ['category_name'], labels = post_labels)
            page_title = "Add Category"
            
            if page_form.accepts(request.vars, session):
                session.flash = "Category added."
                redirect(URL(r = request,f = 'index'))
                
        elif area == "link":
            page_form = SQLFORM(db.links, fields = ['link_title','link_url'], labels = post_labels)
            page_title = "Add Linnk"
            
            if page_form.accepts(request.vars, session):
                session.flash = "Link added."
                redirect(URL(r = request,f = 'index'))
            
        else:
            redirect(URL(r = request,f = 'index'))
            
        return dict(page_title = page_title, page_form = page_form)
    except:
        redirect(URL(r = request,f = 'index'))

def edit():
    if not session.authorized:
        redirect(URL(r=request,f='index'))
        
    try:
        area = request.args[0]
    except:
        redirect(URL(r = request,f = 'index'))
                    
    if area == 'bloginfo':
        this_item = db().select(db.blog_info.ALL)[0]
        edit_form = SQLFORM(db.blog_info, this_item, fields = ['name', 'title', 'description', 'keywords'], showid=False, labels = blog_info_labels)
        edit_title = "Edit Blog Informations"
        
        if edit_form.accepts(request.vars, session):
            session.flash = "Blog information updated."
            redirect(URL(r = request,f = 'index'))
    
    elif area == 'userinfo':
        this_item = db(db.users.id == session.authorized).select(db.users.ALL)[0]
        edit_form = SQLFORM(db.users, this_item, fields = ['alias','email'], showid=False, labels = user_labels)
        edit_title = "Edit User Informatioins"
        if edit_form.accepts(request.vars, session):
            session.flash = "User Information updated."
            redirect(URL(r = request, f = 'index'))
            
        # an hack to make password update a separated part
        pwd_form = form_factory('myform',
                SQLField('old_password','password',requires=IS_NOT_EMPTY()),
                SQLField('new_password','password',requires=IS_NOT_EMPTY()),
                SQLField('new_password_again','password',
                         requires=IS_EXPR("value=='%s'"%request.vars.new_password,
                                              error_message = "Passwords do not match")))
        pwd_title = "Update User Password"
        if pwd_form.accepts(request.vars,session):
            user=db(db.users.id == session.authorized).select()[0]
            if user.password != hashlib.sha1(pwd_form.vars.old_password).hexdigest():
                response.flash = "Invalid old password"
            else:
                user.update_record(password=hashlib.sha1(pwd_form.vars.new_password).hexdigest())
                response.flash = "Password updated"
        
        return dict(edit_form = edit_form, edit_title = edit_title, pwd_form = pwd_form, pwd_title = pwd_title)
    
    else:
        try:
            id = request.args[1]
        except:
            redirect(URL(r = request,f = 'index'))
            
        if area == 'post':
            this_item = db(db.posts.id == id).select()[0]
            edit_form = SQLFORM(db.posts, this_item, fields = ['post_title', 'post_text', 'post_category'], showid=False, labels = post_labels)
            edit_title = "Edit Post"
        
            if edit_form.accepts(request.vars, session):
                session.flash = "Post updated."
                redirect(URL(r = request,f = 'post/%s' %id))
    
        elif area == 'page':
            this_item = db(db.posts.id == id).select()[0]
            edit_form = SQLFORM(db.posts, this_item, fields = ['post_title', 'post_text'], showid=False, labels = post_labels)
            edit_title = "Edit Page"
        
            if edit_form.accepts(request.vars, session):
                session.flash = "Page updated."
                redirect(URL(r = request,f = 'page/%s' %id))
    
        else:
            redirect(URL(r = request,f = 'index'))
    
    return dict(edit_form = edit_form, edit_title = edit_title)

def manage():
    if not session.authorized:
        redirect(URL(r=request,f='index'))
    try: area = request.args[0]
    except: redirect(URL(r = request,f = 'index'))
    
    try: command = request.args[1]
    except: command = ""
        
    if area == 'link':
        rows = db().select(db.links.ALL)
        manage_title = 'Manage Links'

        if command == 'add':
            edit_form = SQLFORM(db.links, labels = link_labels)
            
            if edit_form.accepts(request.vars, session):
                session.flash = "Link added"
                redirect(URL(r = request, f = 'manage/link'))
            else:
                session.flash = "Error"
       
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                this_link = db(db.links.id == id).select()[0]
                edit_form = SQLFORM(db.links, this_link, showid=False)
                
                if edit_form.accepts(request.vars, session):
                    session.flash = "Link updated"
                    redirect(URL(r = request, f = 'manage/link'))
                else:
                    session.flash = "Error"
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.links.id == id).delete()
                session.flash = "Link deleted"
                redirect(URL(r = request, f = 'manage/link'))
    
        else:
            edit_form = ''
            
        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)
    
    elif area == 'category':
        rows = db().select(db.categories.ALL)
        manage_title = 'Manage Categories'
       
        if command == 'add':
            edit_form = SQLFORM(db.categories, labels = cat_labels)
            
            if edit_form.accepts(request.vars, session):
                session.flash = "Category added"
                redirect(URL(r = request, f = 'manage/category'))
            else:
                session.flash = "Error"
        
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                this_cat = db(db.categories.id == id).select()[0]
                edit_form = SQLFORM(db.categories, this_cat, showid=False)
                
                if edit_form.accepts(request.vars, session):
                    session.flash = "Category updated"
                    redirect(URL(r = request, f = 'manage/category'))
                else:
                    session.flash = "Error"
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.categories.id == id).delete()
                session.flash = "Category deleted"
                redirect(URL(r = request, f = 'manage/category'))
        
        else:
            edit_form = ''
            
        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)
    
    elif area == 'post':
        rows = db(db.posts.post_type == 'post').select(db.posts.ALL)
        manage_title = 'Manage Posts'
       
        if command == 'add':
            redirect(URL(r = request, f = 'add/post'))
            
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                redirect(URL(r = request, f = 'edit/post/'+id))
                
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.posts.id == id).delete()
                session.flash = "Post deleted"
                redirect(URL(r = request, f = 'manage/post'))
        else:
            edit_form = ''
            
        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)
                
    elif area == 'comment':
        rows = db(db.posts.post_type == 'post').select(db.posts.ALL)
        manage_title = 'Manage Posts'
       
        if command == 'delete':
            try: id = request.args[2]
            except:
                redirect(URL(r = request, f = 'index'))
            comment = db(db.comments.id == id).select()[0]
            post_id = comment.post_id;
            db(db.comments.id == id).delete()
            session.flash = "Post deleted"
            redirect(URL(r = request, f = 'post/%d' % post_id))
        
    elif area == 'page':
        rows = db(db.posts.post_type == 'page').select(db.posts.ALL)
        manage_title = 'Manage Pages'
       
        if command == 'add':
            redirect(URL(r = request, f = 'add/page'))
        
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                redirect(URL(r = request, f = 'edit/page/'+id))
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.posts.id == id).delete()
                session.flash = "Page deleted"
                redirect(URL(r = request, f = 'manage/page'))
        
        else:
            edit_form = ''
            
        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)
    
    else:
        redirect(URL(r = request,f = 'index'))
    
def login():
    db.users.email.requires=IS_NOT_EMPTY()
    form=SQLFORM(db.users, fields=['email','password'])
    if form.accepts(request.vars, session):
        users=db(db.users.email==form.vars.email)(db.users.password==hashlib.sha1(form.vars.password).hexdigest()).select()
        #print users
        if len(users):
            session.authorized=users[0].id
            session.email=users[0].email
            session.alias=users[0].alias
            session.flash='User logged in'
            redirect(URL(r=request,f='index'))
        else:
            form.errors['password']='User not exists or invalid password'
    return dict(form=form)

def logout():
    session.authorized=None
    session.email=None
    session.alias=None
    session.flash='User logged out'
    redirect(URL(r=request,f='index'))
    
