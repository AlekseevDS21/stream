import streamlit as st
import pandas as pd

def process_data(df):
    # Пример обработки данных: добавление нового столбца
    df['created_at'] = pd.to_datetime(df['created_at'])

# Создание нового столбца с условием
    df['new_column'] = 0  # Инициализация нового столбца

    # Проход по уникальным значениям 'query'
    for query in df['human_query'].unique():
        # Фильтрация по текущему query
        query_df = df[df['human_query'] == query]
        
        # Проверка количества записей
        if len(query_df) > 1:
            # Находим индексы строк с максимальной и минимальной датой
            max_idx = query_df['created_at'].idxmax()
            min_idx = query_df['created_at'].idxmin()
            
            # Проверка условия и обновление нового столбца
            if df.loc[max_idx, 'result_query'] == df.loc[min_idx, 'expected_query']:
                df.loc[max_idx, 'new_column'] = 1
                df.loc[min_idx, 'new_column'] = 1
    return df

def main():
    st.title("Добавьте выгрузку попалерта")

    # Загрузка файла
    uploaded_file = st.file_uploader("Выберите файл", type="csv")
    
    if uploaded_file is not None:
        # Чтение CSV в DataFrame
        df = pd.read_csv(uploaded_file, sep='|')
        st.write("Исходные данные")
        st.write(df)

        # Обработка данных
        processed_df = process_data(df)
        st.write("Обработанные данные")
        st.write(processed_df)

        # Скачивание обработанного файла
        csv = processed_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Скачать обработанный файл",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
