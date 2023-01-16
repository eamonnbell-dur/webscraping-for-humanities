#!/usr/bin/env python
# coding: utf-8

# # `bs4` Basics
# 
# Here is an example of a very simple HTML document:

# ```html
# <html> 
#   <head> 
#     <title>My page</title> 
#   </head> 
#   <body> 
#     <h2>Welcome to my <a href="./index.html">page</a></h2> 
#     <p id="basic" class="stylish small">This is the first paragraph.</p> 
#     <p id="para2" class="unstylish">This is the second paragraph.</p> 
#     <p>This is the third paragraph, which contains a <a href="https://example.com/about.html">link</a> to another page.</p>
#     <!-- this is the end --> 
#   </body> 
# </html>
# ```

# Eventually, we will learn to request arbitrary HTML documents from remote servers, store them to disk, and load them for analysis. But let's keep things simple and assign this document to a variable called `simple_doc`.

# In[1]:


simple_doc = """<html> 
  <head> 
    <title>My page</title> 
  </head> 
  <body> 
    <h2>Welcome to my <a href="./index.html">page</a></h2> 
    <p id="basic" class="stylish small">This is the first paragraph.</p> 
    <p id="para2" class="unstylish">This is the second paragraph.</p> 
    <p>This is the third paragraph, which contains a <a href="https://example.com/about.html">link</a> to another page.</p>
    <!-- this is the end --> 
  </body> 
</html>"""


# Let's we want to retrieve the title of this HTML document, which is stored in text, wrapped in the `<title>` tags. If you already know a bit about Python, you might know how to manipulate strings. Here, the document has been nicely formatted so that we could do something like this, using string methods:

# In[2]:


title_tag = simple_doc.split('\n')[2].strip()
title_tag


# In[3]:


title_contents = title_tag.replace('<title>', '').replace('</title>', '')
title_contents


# One problem with this technique is that we are making too many assumptions about how the string that stores the HTML document is structured, for example, by assuming that the relevant tag is on the third line (`.split('\n')[2]`) of the multi-line string. In fact, many HTML documents are structurally equivalent to each other, even if we remove all the line spacing. So there are no guarantees that the precis structure that we depend on above to identify the information we care about will be preserved in the form that the server provides us with the remote document. 
# 
# At this point, you might say: ''pattern matching is a good opportunity to try out some regular expressions". To which the answer is a qualified, "sure." 

# A better approach is to use Python to do the work of converting the string that stores the HTML document into an abstract representation of the tree structure that is the page's skeleton.
# 
# In general, this step can be done precisely once for each HTML document, so that once it has been completed, we can start to use the features of the Python programming language to navigate the structure of the document - either manually, or, ultimately, programmatically.
# 
# To do this, we use a third-party Python module called `BeautifulSoup`, which can be made available using the following `import` statement:

# In[4]:


import bs4


# In[5]:


soup = bs4.BeautifulSoup(simple_doc)
type(soup)


# Objects of type `bs4.BeautifulSoup` support a wide range of methods that allow us to access elements of the HTML document. For example, the `.find()` method can be used to find the first instance of a tag with the name given in its first argument:

# In[6]:


title = soup.find('title')


# Take care here. Even though the displayed representation of the object called `title` is the same as the HTML markup that generates it, it is not stored as a string.

# In[7]:


title, type(title)


# It is, rather, a `bs4.element.Tag`, which supports methods useful for further manipulation, such as extracting the text attached to the `<title></title>` tag:

# In[8]:


title_text = title.getText()


# **Exercise**: Retrieve the text *content* of the three paragraph tags (`<p></p>`), place them in a Python list, and assign them to the variable `paragraph_texts`. You will need to read about the `.find_all()` method.

# In[9]:


paragraph_texts = [p.getText() for p in soup.find_all('p')]


# 
