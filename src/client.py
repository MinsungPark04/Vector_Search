from elasticsearch import Elasticsearch
    

class ElaAPI:
    es = Elasticsearch(
       [""],
        verify_certs=False,
        http_auth=("", "")
    )

    @classmethod    
    def healthCheck(cls):        
        health = cls.es.cluster.health()        
        print(health)    
    
    @classmethod    
    def allIndex(cls):
        print(cls.es.info())        
        print (cls.es.cat.indices())

    @classmethod
    def vectorSearch(cls, indx, req_keyword, req_knn,  req_rrf):
        res = cls.es.search(
            index=indx,
            query={
                'bool': {
                    **req_keyword
                }
            },
            knn=req_knn,
            rank={
               **req_rrf
            },
            source=['title', 'content']
        )

        took_time = str(res.get('took', {}))
        
        res = res.get('hits', {}).get('hits', [])
        
        return took_time, res
    
    @classmethod
    def createQuery(cls, ks_fields, vs_fields, search_keyword, vector, k_value, n_value, w_value, r_value):
        req_knn = []

        for field in vs_fields:
            kquery = {
                "field": field,
                "query_vector": vector,
                "k": k_value,
                "num_candidates": n_value
            }
            req_knn.append(kquery)


        print(k_value)

        req_keyword = {
            'must': {
                'multi_match': {
                    'query': search_keyword,
                    'fields': ks_fields,
                }
            }
        }

        req_rrf = {
            'rrf': {
                "window_size": w_value,
                "rank_constant": r_value
            }
        }

        return req_keyword, req_knn, req_rrf