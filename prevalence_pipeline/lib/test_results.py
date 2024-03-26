
def testing_results(loaded_data, selected_year, selected_lemma):
    blogs_containing_word = []
    total_blogs = []
    for blog_name, years_words in loaded_data.items():
        for year, text in years_words.items():
            if year==selected_year:
                total_blogs.append(blog_name)
                words = text.split()  
                for word in words:
                    if word==selected_lemma:
                        blogs_containing_word.append({
                            'blog_name': blog_name,
                            'year': int(year),
                            'word': word  
                        })
    return list(set(val for dic in blogs_containing_word for val in dic.values())), set(total_blogs)
