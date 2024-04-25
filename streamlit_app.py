# Import python packages
import streamlit as st, requests, pandas as pd
from snowflake.snowpark.functions import col


st.title("Example Streamlit App :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

order_name = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ',order_name)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON')
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
                                                                      
ingredients_list = st.multiselect(
    'Choose up to 5 ingredeints:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += x + ' '
        st.subheader(x + ' Nutrition Information')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{x}")
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
                values ('""" + ingredients_string + """')"""

    my_insert_stmt = f"""insert into smoothies.public.orders(name_on_order,ingredients) 
                values ('{order_name}','{ingredients_string}')"""
    
    

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {order_name}!',icon="✅")



    
