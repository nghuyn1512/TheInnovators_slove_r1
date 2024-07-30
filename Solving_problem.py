import pulp

# Định nghĩa dữ liệu
full_time_staff = ['An', 'Bình', 'Châu', 'Dương']
part_time_staff = ['Linh', 'Kiệt', 'Giang', 'Hiếu']
days = list(range(1, 29))  # 4 tuần
shifts = ['S', 'T']

prob = pulp.LpProblem("Xếp_lịch_trực", pulp.LpMinimize)

# Biến quyết định
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in full_time_staff + part_time_staff for j in days for k in shifts), cat='Binary')

# Hàm mục tiêu: không có mục tiêu cụ thể, ta đặt mục tiêu bằng 0
prob += 0
#Hard constraints
# Nhân viên toàn thời gian có tối thiêu 18 ca trong 4 tuần
for i in full_time_staff:
    prob += pulp.lpSum(x[i, j, k] for j in days for k in shifts) == 18

# Nhân viên bán thời gian có tối thiểu 10 ca trong 4 tuần
for i in part_time_staff:
    prob += pulp.lpSum(x[i, j, k] for j in days for k in shifts) == 10

# Ca (S) cần 3 nhân viên,ca (T) cần 1 nhân viên.
for j in days:
    prob += pulp.lpSum(x[i, j, 'S'] for i in full_time_staff + part_time_staff) == 3
    prob += pulp.lpSum(x[i, j, 'T'] for i in full_time_staff + part_time_staff) == 1

# Các nhân viên không thể làm 2 ca cùng một ngày
for i in full_time_staff + part_time_staff:
    for j in days:
        prob += x[i, j, 'S'] + x[i, j, 'T'] <= 1

#Soft constraints
# Nhân viên toàn thời gian mong muốn làm 4-5 ca mỗi tuần,tương ứng với 16-20 ca trong 4 tuần
for i in full_time_staff:
    prob += pulp.lpSum(x[i, j, k] for j in days for k in shifts) >= 16
    prob += pulp.lpSum(x[i, j, k] for j in days for k in shifts) <= 20

# Nhân viên bán thời gian mong muốn làm 2-3 ca mỗi tuần,tương ứng với 8-12 ca trong 4 tuần
for i in part_time_staff:
    prob += pulp.lpSum(x[i, j, k] for j in days for k in shifts) >= 8
    prob += pulp.lpSum(x[i, j, k] for j in days for k in shifts) <= 12

# Nhân viên toàn thời gian muốn làm 4-6 ngày liên tiếp
for i in full_time_staff:
    for start_day in range(1, 24):  
        prob += pulp.lpSum(x[i, start_day + offset, k] for offset in range(6) for k in shifts) <= 6

# Nhân viên bán thời gian muốn làm 2-3 ngày liên tiếp
for i in part_time_staff:
    for start_day in range(1, 27):  
        prob += pulp.lpSum(x[i, start_day + offset, k] for offset in range(3) for k in shifts) <= 3

# Giải bài toán
prob.solve()

# In kết quả
for i in full_time_staff + part_time_staff:
    for j in days:
        for k in shifts:
            if x[i, j, k].varValue:
                print(f"{i} làm việc ngày {j} vào ca {k}")
