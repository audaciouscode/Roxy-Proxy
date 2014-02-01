
def evaluate_text_document(content_request):
    if content_request.content_type.lower().startswith('application/pdf'):
        return 1.0
    elif content_request.content_type.lower().startswith('text/html'):
        threshold = 10000.0
        
        size = threshold - float(content_request.content_size)
        
        if size < 0.0:
            size = 0.0
            
        return (1 - (size / threshold)) * 0.75
    
    return 0
