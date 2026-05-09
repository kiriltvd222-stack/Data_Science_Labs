import streamlit as st
import pandas as pd
import urllib.request
import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Налаштування сторінки
st.set_page_config(page_title="NOAA VHI Dashboard", page_icon="🌍", layout="wide")
st.title("Аналіз вегетаційних індексів України (NOAA)")

# Кешоване завантаження та очищення данних
@st.cache_data
def load_and_clean_data():
    # Якщо папки немає - створюємо
    if not os.path.exists('vhi_data'):
        os.makedirs('vhi_data')
    
    # Завантажуємо дані, якщо їх ще немає
    for province_id in range(1, 28):
        existing_files = [f for f in os.listdir('vhi_data') if f.startswith(f"vhi_id_{province_id}_")]
        if not existing_files:
            url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2=2024&type=Mean"
            try:
                vhi_url = urllib.request.urlopen(url)
                text = vhi_url.read().decode('utf-8')
                text = text.replace("<tt><pre>", "").replace("</pre></tt>", "")
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                with open(f"vhi_data/vhi_id_{province_id}_{now}.csv", 'w') as file:
                    file.write(text)
            except Exception as e:
                pass # Ігноруємо помилки мережі для безперебійної роботи

    # Збираємо всі файли
    all_files = [os.path.join('vhi_data', f) for f in os.listdir('vhi_data') if f.endswith('.csv')]
    df_list = []
    province_mapping = {
        1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 
        11: 9, 12: 0, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 
        20: 0, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5
    }
    
    for file in all_files:
        old_id = int(os.path.basename(file).split('_')[2])
        df_temp = pd.read_csv(file, header=1, names=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'])
        df_temp['Area_ID'] = old_id
        df_list.append(df_temp)
        
    if not df_list:
        return pd.DataFrame() # Порожній датафрейм, якщо немає даних

    df = pd.concat(df_list, ignore_index=True)
    df = df.drop(columns=['empty']).dropna()
    df['Year'] = df['Year'].astype(str).str.replace('<br>', '').str.strip()
    df = df[df['Year'] != '']
    df['Year'] = df['Year'].astype(int)
    df['Week'] = df['Week'].astype(int)
    df['VHI'] = df['VHI'].astype(float)
    df = df[df['VHI'] != -1.0]
    df['Area_ID'] = df['Area_ID'].map(province_mapping)
    df = df[df['Area_ID'] != 0] # Видаляємо Київ та Севастополь
    return df

# Завантажуємо дані
with st.spinner("Завантаження та очищення даних (це може зайняти хвилину при першому запуску)..."):
    df = load_and_clean_data()

# Ініціалізація стану
if 'reset' not in st.session_state:
    st.session_state.reset = False

def reset_filters():
    st.session_state.target_index = "VHI"
    st.session_state.prov_id = 1
    st.session_state.week_range = (1, 52)
    st.session_state.year_range = (1981, 2024)
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

# Інтерфейс у сайдбарі
st.sidebar.header("Параметри фільтрації")

target_index = st.sidebar.selectbox("Оберіть індекс:", ["VCI", "TCI", "VHI"], key="target_index")

# Отримуємо унікальні області 
provinces = sorted(df['Area_ID'].unique().tolist()) if not df.empty else []
prov_id = st.sidebar.selectbox("Оберіть область (ID):", provinces, key="prov_id")

week_range = st.sidebar.slider("Інтервал тижнів:", min_value=1, max_value=52, value=(1, 52), key="week_range")

min_year = int(df['Year'].min()) if not df.empty else 1981
max_year = int(df['Year'].max()) if not df.empty else 2024
year_range = st.sidebar.slider("Інтервал років:", min_value=min_year, max_value=max_year, value=(min_year, max_year), key="year_range")

st.sidebar.markdown("---")
st.sidebar.subheader("Сортування таблиці")
sort_asc = st.sidebar.checkbox("За зростанням", key="sort_asc")
sort_desc = st.sidebar.checkbox("За спаданням", key="sort_desc")

st.sidebar.button("Очистити фільтри", on_click=reset_filters)

# Логіка фільтрації та сортування
if not df.empty:
    # Базова фільтрація
    filtered_df = df[
        (df['Area_ID'] == prov_id) & 
        (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) & 
        (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
    ]

    # Логіка сортування 
    if sort_asc and sort_desc:
        st.warning("⚠️ Увімкнено обидва чекбокси сортування. Дані виведено у хронологічному порядку без сортування.")
    elif sort_asc:
        filtered_df = filtered_df.sort_values(by=target_index, ascending=True)
    elif sort_desc:
        filtered_df = filtered_df.sort_values(by=target_index, ascending=False)

    # Відображення у вкладках
    tab1, tab2, tab3 = st.tabs(["📊 Таблиця даних", "📈 Графік динаміки", "🌍 Порівняння областей"])

    with tab1:
        st.subheader(f"Дані {target_index} для області {prov_id}")
        st.dataframe(filtered_df[['Year', 'Week', 'Area_ID', target_index]], use_container_width=True)

    with tab2:
        st.subheader(f"Динаміка {target_index} у часі (Область {prov_id})")
        # Готуємо дані для графіка (хронологічно)
        plot_df = filtered_df.sort_values(by=['Year', 'Week'])
        plot_df['Time'] = plot_df['Year'].astype(str) + " - W" + plot_df['Week'].astype(str)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(plot_df['Time'], plot_df[target_index], color='teal', linewidth=1.5)
        ax.set_xlabel("Час (Рік - Тиждень)")
        ax.set_ylabel(target_index)
        # Ховаємо всі підписи осі X крім кожного 20-го, щоб не було місива
        ax.set_xticks(ax.get_xticks()[::max(1, len(plot_df)//20)])
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with tab3:
        st.subheader(f"Порівняння середнього {target_index} по всіх областях")
        st.markdown(f"*(за період {year_range[0]}-{year_range[1]} роки, тижні {week_range[0]}-{week_range[1]})*")
        
        # Рахуємо середнє значення індексу для кожної області за вибраний період
        compare_df = df[
            (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) & 
            (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
        ]
        mean_data = compare_df.groupby('Area_ID')[target_index].mean().reset_index()
        
        # Виділяємо вибрану область червоним кольором
        colors = ['tomato' if area == prov_id else 'steelblue' for area in mean_data['Area_ID']]
        
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.barplot(data=mean_data, x='Area_ID', y=target_index, palette=colors, ax=ax2)
        ax2.set_xlabel("ID Області")
        ax2.set_ylabel(f"Середній {target_index}")
        # Додаємо лінію загального середнього
        ax2.axhline(mean_data[target_index].mean(), color='red', linestyle='--', alpha=0.5, label='Середнє по країні')
        ax2.legend()
        st.pyplot(fig2)
else:
    st.error("Помилка завантаження даних. Перевірте з'єднання з інтернетом.")