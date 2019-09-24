# ClassBase View

if pass pagination then it's easy in classbase view

in view.py put

```python
paginate_by=number_of_display_perpage
```

in **html** page use following syntax
if you check previous item or note

```python
{% if page_obj.has_previous %}
    <li class="page-item">
        <a class="page-link" href="?page={{ page_obj.previous_page_number }}" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
        </a>
    </li>
{% endif %}
```

if check next of note then 

```python 
{% if page_obj.has_next %}
    <li class="page-item">
        <a class="page-link" href="?page={{ page_obj.next_page_number }}" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
        </a>
    </li>
{% endif %}
```



### INR symbol

```HTML
&#8377; or &#x20B9; <!--Put in html file   -->
```