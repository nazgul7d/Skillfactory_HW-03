from django import template

register = template.Library()

@register.filter()

def censor(word):
    unwanted_words = ['bad_word1', 'bad_word2', 'bad_word3']
    if type(word) == str:
        if word in unwanted_words:
            edited_version =''
            for i in range(len(word)-1):
                edited_version += '*'
            return word[0] + edited_version      
    else:
        raise TypeError('Only string is allowed')
    return word
    