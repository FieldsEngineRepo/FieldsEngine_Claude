    def irr_check_guess(self, guess):
        outcome = self.IRR_OUT_DEFAULT
        cash_flow_vector = np.array(self.cash_flows)
        try:
            irr_guess_vector = np.array([1.0 / (1 + guess) ** (prod_year_num) for prod_year_num in range(len(self.cash_flows))])
            outcome = np.dot(cash_flow_vector, irr_guess_vector)
            ret_val = float(outcome)
        except:
            print 'irr_check_guess: except '
            ret_val = self.IRR_OUT_DEFAULT
        return ret_val

    def irr_get_outcome_sign(self, outcome):
        sign = 1
        if abs(outcome - self.GOAL) < self.IRR_ZERO_range:
            sign = 0
        elif outcome < self.GOAL:
            sign = -1
        return sign

    def irr_check_plus_minus(self, guess):
        check_val = False
        guess_plus = self.irr_check_guess(guess + self.IRR_INCR_MIN)
        guess_minus = self.irr_check_guess(guess - self.IRR_INCR_MIN)
        if self.irr_get_outcome_sign(guess_plus) == -self.irr_get_outcome_sign(guess_minus):
            check_val = True
        return check_val

    def irr_goal_seek(self):
        increment = self.IRR_INCR_MIN
        goal_reached = False
        breakeven_val = self.IRR_OUT_DEFAULT
        last_outcome = 0
        iter_count = 1
        while not goal_reached:
            if iter_count == 1:
                last_outcome = self.irr_check_guess(self.IRR_INIT_GUESS)
                outcome = self.irr_check_guess(self.IRR_INIT_GUESS + self.IRR_INIT_INCR)
                last_guess = self.IRR_INIT_GUESS
                last_increment = self.IRR_INIT_INCR
                try:
                    increment = float(last_increment * outcome) / float(last_outcome - outcome)
                    increment = min(max(-self.IRR_INCR_MAX, increment), self.IRR_INCR_MAX)
                except:
                    iter_count = self.IRR_ITER_MAX
                guess = last_guess + increment
            outcome = self.irr_check_guess(guess)
            sign = self.irr_get_outcome_sign(outcome)
            if self.irr_check_plus_minus(guess):
                breakeven_val = guess
                goal_reached = True
            if sign == 0:
                breakeven_val = guess
                goal_reached = True
            elif iter_count >= self.IRR_ITER_MAX:
                breakeven_val = self.IRR_OUT_DEFAULT
                goal_reached = True
            else:
                last_guess = guess
                last_increment = increment
                try:
                    increment = float(last_increment * outcome) / float(last_outcome - outcome)
                    increment = min(max(-self.IRR_INCR_MAX, increment), self.IRR_INCR_MAX)
                except:
                    iter_count = self.IRR_ITER_MAX
                last_outcome = outcome
                guess = last_guess + increment
                iter_count += 1
        return breakeven_val

    def calc_irr(self):
        self.cash_flows = self.disc_pre_tax_cashflows
        pre_tax_irr     = round(float(self.irr_goal_seek()), 3)
        self.cash_flows = self.disc_post_tax_cashflows
        post_tax_irr    = round(float(self.irr_goal_seek()), 3)
        return pre_tax_irr, post_tax_irr