{% macro render_choice(choice, story_id) %}
<li class="choice-item">
    <a href="{{ url_for('chapter', story_id=story_id, chapter_id=choice.next_chapter_id) }}"
       class="choice-link">
        {{ choice.text }}
    </a>
    {% if choice.sub_choices %}
    <ul class="sub-choices">
        {% for sub_choice in choice.sub_choices %}
            {{ render_choice(sub_choice, story_id) }}
        {% endfor %}
    </ul>
    {% endif %}
</li>
{% endmacro %}