import pandas as pd
from datetime import datetime, timedelta

# 首先，我们创建开始日期和结束日期
start_date = datetime(2022, 11, 7)
end_date = datetime(2022, 12, 31)

# 然后我们创建一个DataFrame，其中包含从开始日期到结束日期的所有日期，每天有1440行（每分钟一行）
data = pd.date_range(start_date, end_date, freq='T')

# 创建DataFrame
df = pd.DataFrame(data, columns=['Datetime'])

# 添加其他列，'%-m/%-d' 是无前导零的月和日
df['Date'] = df['Datetime'].apply(lambda x: x.strftime('%Y/%-m/%-d'))
df['Month-Year'] = df['Datetime'].apply(lambda x: x.strftime('%Y/%-m'))
df['Year'] = df['Datetime'].dt.strftime('%Y')

# 将Datetime列转换为所需的格式
df['Datetime'] = df['Datetime'].apply(lambda x: x.strftime('%Y/%-m/%-d %H:%M'))

# 将DataFrame保存为CSV
df.to_csv('output.csv', index=False, sep=';')
