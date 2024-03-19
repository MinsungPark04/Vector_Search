import streamlit as st


import client
import model_import


def streamlit_main(ElaAPI):
    res = None

    st.title("Search Result")

    with st.sidebar:
        st.header("Tuning")
        model_name = st.text_input("Model")
        search_keyword = st.text_input("Keyword")

        submit_btn = st.button("Submit")

        tab1, tab2, tab3 = st.sidebar.tabs(['field', 'knn', 'rank(rrf)'])
        
        with tab1:
            ks_field = st.text_input("keyword search field")
            ks_add = st.button('add', key='ks_add')

            if ks_add:
                if not hasattr(st.session_state, 'ks_fields'):
                    st.session_state.ks_fields = []
                
                st.session_state.ks_fields.append(ks_field)

            if hasattr(st.session_state, 'ks_fields'):
                selected_ks_fields = st.multiselect('keyword search select fields', options=st.session_state.ks_fields, default=st.session_state.ks_fields)
                st.session_state.ks_fields = selected_ks_fields

            vs_field = st.text_input("vector search field")
            vs_add = st.button('add', key='vs_add')

            if vs_add:
                if not hasattr(st.session_state, 'vs_fields'):
                    st.session_state.vs_fields = []
                
                st.session_state.vs_fields.append(vs_field)

            if hasattr(st.session_state, 'vs_fields'):
                selected_vs_fields = st.multiselect('vector search select fields', options=st.session_state.vs_fields, default=st.session_state.vs_fields)
                st.session_state.vs_fields = selected_vs_fields       


        with tab2:
            k_value = st.slider('k', 1, 100, 10, 1)
            n_value = st.slider('num_cadidates', 100, 10000, 10000, 100)

        with tab3:
            w_value = st.slider('window_size', 1, 100, 50, 1)
            r_value = st.slider('rank_constant', 1, 100, 20, 1)

        if submit_btn:
            if not model_name:
                st.markdown("<span style='color:red'>모델을 선택해주세요.</span>", unsafe_allow_html=True)
                return

            if not search_keyword:
                st.markdown("<span style='color:red'>검색어를 입력해주세요.</span>", unsafe_allow_html=True)
                return
            
            ks_fields = st.session_state.ks_fields if hasattr(st.session_state, 'ks_fields') else []
            vs_fields = st.session_state.vs_fields if hasattr(st.session_state, 'vs_fields') else []

        
            vector = model_import.get_embedding(model_name=model_name, search_keyword=search_keyword)
        

            print(ks_fields)
            req_keyword, req_knn,  req_rrf = ElaAPI.createQuery(ks_fields=ks_fields, vs_fields=vs_fields , search_keyword=search_keyword, vector=vector, k_value=k_value, n_value=n_value, w_value=w_value, r_value=r_value)

            took_time, res = ElaAPI.vectorSearch(indx="nlp_search_naver_news_1", req_keyword=req_keyword, req_knn=req_knn,  req_rrf=req_rrf)


    if res is not None:
        st.json(res)        


if __name__ == '__main__':
    ElaAPI = client.ElaAPI()
    streamlit_main(ElaAPI)