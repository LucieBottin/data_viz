import streamlit as st
# importing numpy and pandas for to work with sample data.
import numpy as np
import pandas as pd 
import time

st.title('My first app')
st.text('Hello to everyone')
st.markdown("yo les **giga** kheys")
st.caption("je suis une caption")
st.latex(r'''a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k = a \left(\frac{1-r^{n}}{1-r}\right)''')

df = pd.DataFrame({
'first column': [1, 2, 3, 4],
'second column': [10, 20, 30, 40]
})
st.write(df)
st.dataframe(df.style.highlight_max(axis=0))
st.table(df)
st.metric(label="Temperature", value="20°C", delta="-10 °C")

chart_data = pd.DataFrame(
np.random.randn(20, 3),
columns=['a', 'b', 'c'])
st.line_chart(chart_data)
st.area_chart(chart_data)
st.bar_chart(chart_data)

df_map = pd.df[['lat', 'long']]
st.map(df_map)

if st.button('Say hello'):
    st.write('Hello there')
else:
    st.write('Goodbye')

agree = st.checkbox('I agree')

if agree:
    st.write('Great!')

genre = st.radio(
    "Avez-vous des amis ?",
    ('Oui', 'Non', 'J''essaie'))

if genre == 'Oui':
    st.write('You selected Oui.')
else:
    st.write("You didn't select comedy.")

option = st.selectbox(
     'Quel est votre genre ?',
     ('Femme', 'Homme', 'Non binaire', 'Bad bitch'))

st.write('You selected:', option)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
    chart_data

option = st.selectbox(
'Which number do you like best?', df['first column'])
'You selected: ', option

left_column, right_column = st.columns(2)
pressed = left_column.button('Tu veux une énigme ?')
if pressed:
    right_column.write("Let's go!")
    expander = st.expander("Enigme")
    expander.write("Qu'est ce qui est jaune et qui attend ?")

latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Ca chaaaaaarge : {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)
'...CEST BONNNN!'