# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
# from .models import Doubt

# # doubts=Index('doubts')
# @registry.register_document
# # @doubts.document
# class DoubtDocument(Document):
#     # title = fields.TextField() 
#     class Index:
#         title='doubt'  
    
#     settings={
#         'number_of_shards':1,
#         'number_of_replicas':0
#     }
#     class Django:
#         model=Doubt
#         fields=['title','description']

#         # def get_queryset(self):
#         #     return super(DoubtDocument, self).get_queryset().select_related('title')

