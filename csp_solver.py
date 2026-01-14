import csv
import math

class CSPSolver:
    def __init__(self):
        self.nva = 0  # Number of variable assignments
        self.solution = None
    
    def solve_problem_a(self):
        """
        Solve Problem A with constraints C1-C5:
        C1: A = B² - C²
        C2: C + E > B
        C3: D = B² - 4A
        C4: (B-C)² = E*F*B - 396
        C5: C + D + E + F < 125
        """
        # Search over B and C first since they determine A and D
        for B in range(1, 121):
            self.nva += 1
            
            # From C1: A = B² - C²
            # We need A ≥ 1, so B² - C² ≥ 1, thus C² ≤ B² - 1
            # This means C < B (approximately)
            
            # From C4: (B-C)² = E*F*B - 396
            # We need (B-C)² + 396 = E*F*B
            # So (B-C)² + 396 must be divisible by B
            
            for C in range(1, B + 1):  # C should be ≤ B for reasonable A values
                self.nva += 1
                
                # Calculate A from C1
                A = B**2 - C**2
                if A < 1 or A > 120:
                    continue
                
                # Calculate D from C3
                D = B**2 - 4*A
                if D < 1 or D > 120:
                    continue
                
                # Verify D = -3B² + 4C²
                D_check = -3*B**2 + 4*C**2
                if D != D_check:
                    continue
                
                # From C2: E ≥ B - C + 1
                E_min = max(1, B - C + 1)
                
                # From C5: C + D + E + F < 125
                # So E + F < 125 - C - D
                max_EF_sum = 125 - C - D - 1  # -1 because we need strict inequality
                
                if max_EF_sum < E_min + 1:  # Need at least E_min + 1 (for F≥1)
                    continue
                
                # From C4: (B-C)² + 396 = E*F*B
                target = (B - C)**2 + 396
                
                if target % B != 0:
                    continue
                
                EF_product = target // B
                
                # Find E and F such that E*F = EF_product
                # E must be in [E_min, max_EF_sum - 1] and within [1, 120]
                E_max = min(EF_product, max_EF_sum - 1, 120)
                
                for E in range(E_min, E_max + 1):
                    self.nva += 1
                    
                    if EF_product % E != 0:
                        continue
                    
                    F = EF_product // E
                    self.nva += 1
                    
                    if F < 1 or F > 120:
                        continue
                    
                    # Check C2: C + E > B
                    if C + E <= B:
                        continue
                    
                    # Check C5: C + D + E + F < 125
                    if C + D + E + F >= 125:
                        continue
                    
                    # Found a solution!
                    self.solution = {
                        'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F
                    }
                    return True
        
        return False
    
    def solve_problem_b(self):
        """
        Solve Problem B with constraints C1-C12 involving variables A-J:
        C1: A = B² - C²
        C2: C + E > B
        C3: D = B² - 4A
        C4: (B-C)² = E*F*B - 396
        C5: C + D + E + F < 125
        C6: (G+I)³ - 4 = (H-A)²
        C7: C*E*F + 40 = (H-F-I)*(I+G)
        C8: (C+I)² = B*E*(I+3)
        C9: G + I < E + 3
        C10: D + H > 180
        C11: J < D + E + F
        C12: J > H + E + F + G + I
        """
        # First, find valid solutions for A-F from Problem A constraints
        for B in range(1, 121):
            self.nva += 1
            
            for C in range(1, B + 1):
                self.nva += 1
                
                # Calculate A from C1
                A = B**2 - C**2
                if A < 1 or A > 120:
                    continue
                
                # Calculate D from C3
                D = B**2 - 4*A
                if D < 1 or D > 120:
                    continue
                
                # From C2: E ≥ B - C + 1
                E_min = max(1, B - C + 1)
                
                # From C5: E + F < 125 - C - D
                max_EF_sum = 125 - C - D - 1
                
                if max_EF_sum < E_min + 1:
                    continue
                
                # From C4: (B-C)² + 396 = E*F*B
                target = (B - C)**2 + 396
                
                if target % B != 0:
                    continue
                
                EF_product = target // B
                E_max = min(EF_product, max_EF_sum - 1, 120)
                
                for E in range(E_min, E_max + 1):
                    self.nva += 1
                    
                    if EF_product % E != 0:
                        continue
                    
                    F = EF_product // E
                    self.nva += 1
                    
                    if F < 1 or F > 120:
                        continue
                    
                    # Check C2 and C5
                    if C + E <= B:
                        continue
                    if C + D + E + F >= 125:
                        continue
                    
                    # Now we have valid A, B, C, D, E, F
                    # Search for G, H, I, J
                    
                    # From C9: G + I < E + 3, so G + I ≤ E + 2
                    max_GI_sum = E + 2
                    
                    for G in range(1, min(121, max_GI_sum)):
                        self.nva += 1
                        
                        # From C9: I < E + 3 - G
                        I_max = min(120, E + 2 - G)
                        
                        for I in range(1, I_max + 1):
                            self.nva += 1
                            
                            # Check C9: G + I < E + 3
                            if G + I >= E + 3:
                                continue
                            
                            # From C8: (C+I)² = B*E*(I+3)
                            left_c8 = (C + I)**2
                            right_c8 = B * E * (I + 3)
                            if left_c8 != right_c8:
                                continue
                            
                            # From C6: (G+I)³ - 4 = (H-A)²
                            # So (H-A)² = (G+I)³ - 4
                            GI_cubed_minus_4 = (G + I)**3 - 4
                            
                            if GI_cubed_minus_4 < 0:
                                continue
                            
                            # H - A = ±sqrt(GI_cubed_minus_4)
                            sqrt_val = GI_cubed_minus_4 ** 0.5
                            
                            if sqrt_val != int(sqrt_val):
                                continue
                            
                            sqrt_val = int(sqrt_val)
                            
                            # Try both H = A + sqrt_val and H = A - sqrt_val
                            for H in [A + sqrt_val, A - sqrt_val]:
                                self.nva += 1
                                
                                if H < 1 or H > 120:
                                    continue
                                
                                # Check C10: D + H > 180
                                if D + H <= 180:
                                    continue
                                
                                # From C7: C*E*F + 40 = (H-F-I)*(I+G)
                                left_c7 = C * E * F + 40
                                right_c7 = (H - F - I) * (I + G)
                                if left_c7 != right_c7:
                                    continue
                                
                                # From C11: J < D + E + F
                                J_max = D + E + F - 1
                                
                                # From C12: J > H + E + F + G + I
                                J_min = H + E + F + G + I + 1
                                
                                if J_min > J_max:
                                    continue
                                
                                # Find valid J
                                for J in range(max(1, J_min), min(121, J_max + 1)):
                                    self.nva += 1
                                    
                                    # Found a solution!
                                    self.solution = {
                                        'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F,
                                        'G': G, 'H': H, 'I': I, 'J': J
                                    }
                                    return True
        
        return False
    
    def solve_problem_c(self):
        """
        Solve Problem C with constraints C1-C17 involving variables A-M:
        C1-C12: Same as Problem B
        C13: K*L*M = B*(K+5)
        C14: F³ = K²*(L-29) + 25
        C15: H*M² = L*G - 3
        C16: J + M = (L-15)*(E+G)
        C17: K³ = (J-4)*(L-20)
        """
        # First, find valid solutions for A-J from Problem B constraints
        for B in range(1, 121):
            self.nva += 1
            
            for C in range(1, B + 1):
                self.nva += 1
                
                # Calculate A from C1
                A = B**2 - C**2
                if A < 1 or A > 120:
                    continue
                
                # Calculate D from C3
                D = B**2 - 4*A
                if D < 1 or D > 120:
                    continue
                
                # From C2: E ≥ B - C + 1
                E_min = max(1, B - C + 1)
                
                # From C5: E + F < 125 - C - D
                max_EF_sum = 125 - C - D - 1
                
                if max_EF_sum < E_min + 1:
                    continue
                
                # From C4: (B-C)² + 396 = E*F*B
                target = (B - C)**2 + 396
                
                if target % B != 0:
                    continue
                
                EF_product = target // B
                E_max = min(EF_product, max_EF_sum - 1, 120)
                
                for E in range(E_min, E_max + 1):
                    self.nva += 1
                    
                    if EF_product % E != 0:
                        continue
                    
                    F = EF_product // E
                    self.nva += 1
                    
                    if F < 1 or F > 120:
                        continue
                    
                    # Check C2 and C5
                    if C + E <= B:
                        continue
                    if C + D + E + F >= 125:
                        continue
                    
                    # From C9: G + I < E + 3
                    max_GI_sum = E + 2
                    
                    for G in range(1, min(121, max_GI_sum)):
                        self.nva += 1
                        
                        I_max = min(120, E + 2 - G)
                        
                        for I in range(1, I_max + 1):
                            self.nva += 1
                            
                            if G + I >= E + 3:
                                continue
                            
                            # C8: (C+I)² = B*E*(I+3)
                            if (C + I)**2 != B * E * (I + 3):
                                continue
                            
                            # C6: (G+I)³ - 4 = (H-A)²
                            GI_cubed_minus_4 = (G + I)**3 - 4
                            
                            if GI_cubed_minus_4 < 0:
                                continue
                            
                            sqrt_val = GI_cubed_minus_4 ** 0.5
                            
                            if sqrt_val != int(sqrt_val):
                                continue
                            
                            sqrt_val = int(sqrt_val)
                            
                            for H in [A + sqrt_val, A - sqrt_val]:
                                self.nva += 1
                                
                                if H < 1 or H > 120:
                                    continue
                                
                                # C10: D + H > 180
                                if D + H <= 180:
                                    continue
                                
                                # C7: C*E*F + 40 = (H-F-I)*(I+G)
                                if C * E * F + 40 != (H - F - I) * (I + G):
                                    continue
                                
                                # C11 and C12 bounds for J
                                J_max = D + E + F - 1
                                J_min = H + E + F + G + I + 1
                                
                                if J_min > J_max:
                                    continue
                                
                                for J in range(max(1, J_min), min(121, J_max + 1)):
                                    self.nva += 1
                                    
                                    # Now search for K, L, M
                                    # From C17: K³ = (J-4)*(L-20)
                                    # So (J-4)*(L-20) must be a perfect cube
                                    
                                    for K in range(1, 121):
                                        self.nva += 1
                                        
                                        K_cubed = K**3
                                        
                                        # From C17: K³ = (J-4)*(L-20)
                                        # So L = K³/(J-4) + 20
                                        if J == 4:
                                            if K_cubed == 0:  # Would need K=0, invalid
                                                continue
                                            else:
                                                continue
                                        
                                        if K_cubed % (J - 4) != 0:
                                            continue
                                        
                                        L = K_cubed // (J - 4) + 20
                                        self.nva += 1
                                        
                                        if L < 1 or L > 120:
                                            continue
                                        
                                        # From C14: F³ = K²*(L-29) + 25
                                        left_c14 = F**3
                                        right_c14 = K**2 * (L - 29) + 25
                                        if left_c14 != right_c14:
                                            continue
                                        
                                        # From C13: K*L*M = B*(K+5)
                                        # So M = B*(K+5)/(K*L)
                                        if K == 0 or L == 0:
                                            continue
                                        
                                        if (B * (K + 5)) % (K * L) != 0:
                                            continue
                                        
                                        M = (B * (K + 5)) // (K * L)
                                        self.nva += 1
                                        
                                        if M < 1 or M > 120:
                                            continue
                                        
                                        # C15: H*M² = L*G - 3
                                        if H * M**2 != L * G - 3:
                                            continue
                                        
                                        # C16: J + M = (L-15)*(E+G)
                                        if J + M != (L - 15) * (E + G):
                                            continue
                                        
                                        # Found a solution!
                                        self.solution = {
                                            'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F,
                                            'G': G, 'H': H, 'I': I, 'J': J, 'K': K, 'L': L, 'M': M
                                        }
                                        return True
        
        return False
    def verify_solution(self, sol, problem='A'):
        """Verify the solution satisfies all constraints"""
        if problem == 'A':
            A, B, C, D, E, F = sol['A'], sol['B'], sol['C'], sol['D'], sol['E'], sol['F']
            
            checks = {
                'C1': A == B**2 - C**2,
                'C2': C + E > B,
                'C3': D == B**2 - 4*A,
                'C4': (B - C)**2 == E*F*B - 396,
                'C5': C + D + E + F < 125
            }
        elif problem == 'B':
            A, B, C, D, E, F = sol['A'], sol['B'], sol['C'], sol['D'], sol['E'], sol['F']
            G, H, I, J = sol['G'], sol['H'], sol['I'], sol['J']
            
            checks = {
                'C1': A == B**2 - C**2,
                'C2': C + E > B,
                'C3': D == B**2 - 4*A,
                'C4': (B - C)**2 == E*F*B - 396,
                'C5': C + D + E + F < 125,
                'C6': (G + I)**3 - 4 == (H - A)**2,
                'C7': C*E*F + 40 == (H - F - I)*(I + G),
                'C8': (C + I)**2 == B*E*(I + 3),
                'C9': G + I < E + 3,
                'C10': D + H > 180,
                'C11': J < D + E + F,
                'C12': J > H + E + F + G + I
            }
        elif problem == 'C':
            A, B, C, D, E, F = sol['A'], sol['B'], sol['C'], sol['D'], sol['E'], sol['F']
            G, H, I, J = sol['G'], sol['H'], sol['I'], sol['J']
            K, L, M = sol['K'], sol['L'], sol['M']
            
            checks = {
                'C1': A == B**2 - C**2,
                'C2': C + E > B,
                'C3': D == B**2 - 4*A,
                'C4': (B - C)**2 == E*F*B - 396,
                'C5': C + D + E + F < 125,
                'C6': (G + I)**3 - 4 == (H - A)**2,
                'C7': C*E*F + 40 == (H - F - I)*(I + G),
                'C8': (C + I)**2 == B*E*(I + 3),
                'C9': G + I < E + 3,
                'C10': D + H > 180,
                'C11': J < D + E + F,
                'C12': J > H + E + F + G + I,
                'C13': K*L*M == B*(K + 5),
                'C14': F**3 == K**2*(L - 29) + 25,
                'C15': H*M**2 == L*G - 3,
                'C16': J + M == (L - 15)*(E + G),
                'C17': K**3 == (J - 4)*(L - 20)
            }
        else:
            return False, {}
        
        
        return all(checks.values()), checks
    
    def save_to_csv(self, problem_name, filename='csp_solution.csv'):
        """Save solution to CSV file"""
        if self.solution is None:
            print(f"No solution found for {problem_name}")
            return
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Variable', 'Value'])
            for var, val in sorted(self.solution.items()):
                writer.writerow([var, val])
        
        print(f"Solution saved to {filename}")
    
    def print_results(self, problem_name):
        """Print results"""
        print(f"\n{'='*50}")
        print(f"Problem {problem_name} Results")
        print(f"{'='*50}")
        
        if self.solution:
            print("Solution found:")
            for var, val in sorted(self.solution.items()):
                print(f"  {var} = {val}")
            
            # Verify
            all_valid, checks = self.verify_solution(self.solution, problem_name)
            print(f"\nVerification:")
            for constraint, valid in checks.items():
                print(f"  {constraint}: {'✓' if valid else '✗'}")
            print(f"  Overall: {'✓ VALID' if all_valid else '✗ INVALID'}")
        else:
            print("No solution exists")
        
        print(f"\nNumber of variable assignments (nva): {self.nva}")
        print(f"{'='*50}\n")


def solve_csp(problem='A'):
    """
    Main interface to solve CSP problems
    
    Args:
        problem: 'A', 'B', or 'C'
    
    Returns:
        tuple: (solution_dict or None, nva)
    """
    solver = CSPSolver()
    
    if problem == 'A':
        found = solver.solve_problem_a()
        solver.print_results('A')
        if found:
            solver.save_to_csv('A')
        return solver.solution, solver.nva
    elif problem == 'B':
        found = solver.solve_problem_b()
        solver.print_results('B')
        if found:
            solver.save_to_csv('B')
        return solver.solution, solver.nva
    elif problem == 'C':
        found = solver.solve_problem_c()
        solver.print_results('C')
        if found:
            solver.save_to_csv('C')
        return solver.solution, solver.nva
    else:
        print(f"Problem {problem} not yet implemented")
        return None, 0


# Example usage
if __name__ == "__main__":
    import sys
    
    # Allow command line argument to specify problem
    problem = sys.argv[1] if len(sys.argv) > 1 else 'A'
    
    print(f"CSP Solver - Problem {problem}")
    print("Solving constraint satisfaction problem...\n")
    
    solution, nva = solve_csp(problem)
    
    if solution:
        print("\nFinal solution:")
        print(solution)
    else:
        print("\nNo solution found")
    
    print(f"Total variable assignments: {nva}")