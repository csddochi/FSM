module tb_and_test(reset, clk, i2, i1);
	input reset, clk, i2, i1;
	parameter s1 = 0, s2 = 500, s3 = 1000, s4 = 1500, s5 = 2000, s6 = 2300, s7 = 2800, s8 = 3000, s9 = 3300, s10 = 3500, s11 = 4000, s12 = 4500;
	reg[1:0] state, nextState;

	always @(posedge clk) begin
		if(reset) begin
			state <= s1;
			i2 = 0, i1 = 0;
		end
		else begin
			state <= nextState;
		end
	end

	always @(i2, i1) begin
		case(state)
		s1 : begin
			if(i1 == 1) nextState <= s2;
			else nextState <= s1;
		end
		s2 : begin
			if(i2 == 1) nextState <= s3;
			else nextState <= s1;
		end
		s3 : begin
			if(i1 == 0) nextState <= s4;
			else nextState <= s1;
		end
		s4 : begin
			if(i2 == 0) nextState <= s5;
			else nextState <= s1;
		end
		s5 : begin
			if(i1 == 1) nextState <= s6;
			else nextState <= s1;
		end
		s6 : begin
			if(i2 == 1) nextState <= s7;
			else nextState <= s1;
		end
		s7 : begin
			if(i1 == 0) nextState <= s8;
			else nextState <= s1;
		end
		s8 : begin
			if(i2 == 0) nextState <= s9;
			else nextState <= s1;
		end
		s9 : begin
			if(i2 == 1) nextState <= s10;
			else nextState <= s1;
		end
		s10 : begin
			if(i1 == 1) nextState <= s11;
			else nextState <= s1;
		end
		s11 : begin
			if(i1 == 0) nextState <= s12;
			else nextState <= s1;
		end
		s12 : begin
			nextState <= s1;
		end
		endcase
	end
endmodule