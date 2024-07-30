import pulp

# Define data
full_time_staff = ['An', 'Binh', 'Chau', 'Duong']
part_time_staff = ['Linh', 'Kiet', 'Giang', 'Hieu']
days = list(range(28))  # 4 weeks
shifts = ['day', 'night']

# Create problem instance
prob = pulp.LpProblem("Staff_Scheduling", pulp.LpMinimize)

# Decision variables
# x[i][j][k] is 1 if staff i works on day j at shift k, 0 otherwise
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in full_time_staff + part_time_staff for j in days for k in shifts), cat='Binary')

# Objective function: Minimize the total number of shifts that do not meet the staffing requirements
# Here we don't have a specific objective, so we set it to 0
prob += 0

# Constraints
# Full-time staff work 36 hours per week (4 weeks)
for i in full_time_staff:
    prob += pulp.lpSum(x[i, j, 'day'] + x[i, j, 'night'] for j in days) == 18

# Part-time staff work 20 hours per week (4 weeks)
for i in part_time_staff:
    prob += pulp.lpSum(x[i, j, 'day'] + x[i, j, 'night'] for j in days) == 10

# Each shift requires specific staffing
for j in days:
    prob += pulp.lpSum(x[i, j, 'day'] for i in full_time_staff + part_time_staff) == 3
    prob += pulp.lpSum(x[i, j, 'night'] for i in full_time_staff + part_time_staff) == 1

# No overlapping shifts for any staff member
for i in full_time_staff + part_time_staff:
    for j in days:
        prob += x[i, j, 'day'] + x[i, j, 'night'] <= 1

# Solve the problem
prob.solve()

# Print results
for i in full_time_staff + part_time_staff:
    for j in days:
        for k in shifts:
            if x[i, j, k].varValue:
                print(f"{i} works on day {j} at {k} shift")
