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
#     <h2>Welcome to my <a href="https://example.com/index.html">page</a></h2> 
#     <p id="para1" class="stylish small">This is the first paragraph.</p> 
#     <p id="para2" class="unstylish small">This is the second paragraph.</p> 
#     <p id="para3"> This is the third paragraph, which contains a <a href="https://example.com/about.html">link</a> to another page.</p>
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
    <h2>Welcome to my <a href="https://example.com/index.html">page</a></h2> 
    <p id="para1" class="stylish small">This is the first paragraph.</p> 
    <p id="para2" class="unstylish small">This is the second paragraph.</p> 
    <p id="para3"> This is the third paragraph, which contains a <a href="https://example.com/about.html">link</a> to another page.</p>
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

# A better approach is to use Python to do the work of converting the string that stores the HTML document into an abstract representation of the tree structure that is the page's skeleton.
# 
# In general, this step can be done precisely once for each HTML document, so that once it has been completed, we can start to use the features of the Python programming language to navigate the structure of the document - either manually, or, ultimately, programmatically.
# 
# To do this, we use a third-party Python module called `BeautifulSoup`, which can be made available using the following `import` statement:

# In[4]:


import bs4


# We ask `bs4` to process the string that stores the HTML document and return a new Python object, that we will call `soup` throughout:

# In[5]:


soup = bs4.BeautifulSoup(simple_doc.replace('\n', ''))
type(soup)


# Objects of type `bs4.BeautifulSoup` support a wide range of methods that allow us to access elements of the HTML document. For example, the `.find()` method can be used to find the first instance of a tag with the name given in its first argument:

# In[6]:


title = soup.find('title')


# Take care here. Even though the displayed representation of the object called `title` is the same as the HTML markup that generates it, it is not stored as a string.

# In[7]:


title, type(title)


# It is, rather, a `bs4.element.Tag`, which supports methods useful for further manipulation, such as extracting the text attached to the `<title></title>` tag:

# In[8]:


title_text = title.get_text()


# We can also use methods on the `bs4.element.Tag` in order to retrieve elements that have a specific relationship to it within the HTML document, such as this method, which finds the parent of the element given: the `<head>` element. This method returns the whole subdocument enclosed by the relevant tags.

# In[9]:


title.findParent()


# **NB** In fact, we can use many methods on the subdocuments returned from the result of a method. This means that almost all of the methods that the `soup` object supports - such as `.find()` can be called on the outputs of these methods. This allows you to "zoom in" on the part of the HTML document that you care about. This will become especially important in the next set of examples.

# The `find_next_sibling()` method can be used to find sibling elements, which are those at the same level in the document tree. They will be returned in the order that they appear in the document at that level. In this example, it is in the paragraph ordered.

# In[10]:


h2_next_sibling = soup.body.h2.find_next_sibling()
h2_next_sibling, h2_next_sibling.get_text()


# The `find_next_siblings()` method is a shortcut to return all siblings, which will be wrapped in a `ResultSet`, which behaves a little like a regular Python `list`.

# In[11]:


h2_next_siblings = soup.body.h2.find_next_siblings()
h2_second_sibling = h2_next_siblings[1]
h2_second_sibling


# This has consequences for how you might choose to manipulate the result. `bs4` provides a helpful message here to help you out of the issue.

# In[12]:


h2_next_siblings.text


# In[13]:


h2_next_siblings_texts = [x.get_text() for x in h2_next_siblings]
h2_next_siblings_texts


# **Self-check 1**: 
# 
# Retrieve the text *content* of the three paragraph tags (`<p></p>`), place them in a Python list, and assign them to the variable `paragraph_texts`. You will need to read about the `.find_all()` method.
# 
# **Solution**:

# In[14]:


paragraph_texts = [p.get_text() for p in soup.find_all('p')]
paragraph_texts


# It's worth noting that this gives the same result as looking at the text attribute of `h2_next_siblings_texts`. 

# In[15]:


assert(h2_next_siblings_texts == paragraph_texts)


# What's important to note is that the same result can be achieved by many different means: in the first instance, we arrive at the relevant `p` elements through their relative position with respect to the `h2` element that precedes them, whereas in the second example, we simply ask for all `p` elements in the document. 
# 
# Depending on your application, and depending on how frequently you expect the site you are scraping to change, different options will be appropriate.

# **Self-check 2**: 
# 
# Retrieve the link *destination* of all the hyperlinks in the document `<body`> and place them in a Python list, and assign them to the variable `document_links`. You will need to address the `href` attribute of each of the `<a>` elements you find.
# 
# **Solution**:

# In[16]:


document_links = [a.attrs['href'] for a in soup.body.find_all('a')]
document_links


# The destination of hyperlinks is stored in the `href` attribute of a tag. There is often other useful information stored in the tag attributes. Specificially:
# 
# - The `class` attribute contains information that is frequently used to modify the appearance of a HTML element in the browser (using a technology called CSS, which we do not need to deal with here)
# - The `id` attribute contains information that is frequently used to make a page interactive (using JavaScript and frontend frameworks), and to modify the appearance of a HTML element in the browser (using CSS)
# 
# 
# For example, the second paragraph tag contains some of this information:
# 
# ```html
# <p id="para1" class="stylish small">This is the first paragraph.</p> 
# ```
# 
# - The `class` attribute contains two values, separated by a space: `stylish` and `small`. 
# - The `id` attribute contains one value, `para1`.

# We can use `.find_all` with some additional arguments to use `bs4` to find tags in a parsed HTML document according to their attribute values. 

# In[17]:


soup.find_all('p', id='para1')


# In[18]:


soup.find_all('p', id='para2')


# Note that if you are trying to filter on the value of the element's `class` attribute, you will have to use the keyword argument `class_`, a naming decision made to avoid a clash with the reserved word `class`:

# In[19]:


soup.find_all('p', class='small')


# When you search for a tag that matches a certain CSS class, you’re matching against any of its CSS classes:

# In[ ]:


soup.find_all('p', class_='small')


# You can also filter an attribute using a regular expression...

# In[ ]:


import re
soup.find_all('p', id=re.compile('para[2-3]'))


# ...or a list.

# In[ ]:


soup.find_all('p', class_=['stylish', 'unstylish'])


# We might like to keep all the information about the HTML document together, and one way to do this is to use a Python `dict`, which allows you to define record types. Let's say that for every HTML document we might scrape, we care about the following information:
# 
# - The title of the document
# - The content of the first `h2` element in the document
# - The number of links the document contains
# 

# In[ ]:


record = {
    "title_text": soup.title.get_text(),
    "h2_text" : soup.find('h2').get_text(),
    "num_links" : len(soup.find_all('a'))
}


# In[ ]:


record


# We are now in a position to tie all of the above into a short function that takes as its input a string storing a HTML document, parses the document using `bs4`, and returns a `dict` with the relevant information in it.

# In[ ]:


def get_record_for_document(html_doc):
    soup = bs4.BeautifulSoup(html_doc)
    record = {
        "title_text": soup.title.get_text(),
        "h2_text" : soup.find('h2').get_text(),
        "num_links" : len(soup.find_all('a'))
    }

    return record


# Let's define another simple HTML document. (Again, you will eventually retrieve these yourself from the web.)

# In[ ]:


another_simple_doc = """<html> 
  <head> 
    <title>My other page</title> 
  </head> 
  <body> 
    <h2>Welcome to my <a href="https://example.com/index.html">other page</a></h2> 
    <p id="para1" class="stylish small">This is the <a href="https://example.com/contact.html">place you can contact me</a>.</p> 
    <p id="para2"> This is the third paragraph, which contains a <a href="https://example.com/about.html">link</a> to another page.</p>
    <!-- this is the end --> 
  </body> 
</html>"""


# We use our function to produce a list of records from the documents we have to hand:

# In[ ]:


records = [get_record_for_document(simple_doc), get_record_for_document(another_simple_doc)]
records


# Finally, we see the usefulness of using `dicts` to store record information, as it allows us to use Python's built-in `csv` library to store the records to disk in the plain-text comma-separated value (CSV) format, so that it may be consumed by other applications. 

# In[ ]:


import csv

with open('bs4-basics-results.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=records[0].keys())

    writer.writeheader()
    writer.writerows(records)


# In[ ]:


get_ipython().system('head bs4-basics-results.csv')

