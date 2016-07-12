module tb_and_test(reset, clk, i4, i3, i1, i2);
	input reset, clk, i4, i3, i1, i2;
	parameter s1 = 0, s2 = 200, s3 = 700, s4 = 900, s5 = 1000, s6 = 1300, s7 = 1800, s8 = 2300, s9 = 2800, s10 = 3100, s11 = 3400, s12 = 3600, s13 = 3800, s14 = 4100;
	reg[1:0] state, nextState;

	always @(posedge clk) begin
		if(reset) begin
			state <= s1;
			i4 = 0, i3 = 0, i1 = 0, i2 = 0;
		end
		else begin
			state <= nextState;
		end
	end

	always @(i4, i3, i1, i2) begin
		case(state)
		s1 : begin
			if(i3 == 1) nextState <= s2;
			else nextState <= s1;
		end
		s2 : begin
			if(i1 == 1) nextState <= s3;
			else nextState <= s1;
		end
		s3 : begin
			if(i3 == 0) nextState <= s4;
			else nextState <= s1;
		end
		s4 : begin
			if(i4 == 1) nextState <= s5;
			else nextState <= s1;
		end
		s5 : begin
			if(i1 == 0) nextState <= s6;
			else nextState <= s1;
		end
		s6 : begin
			if(i2 == 1) nextState <= s7;
			else nextState <= s1;
		end
		s7 : begin
			if(i1 == 1) nextState <= s8;
			else nextState <= s1;
		end
		s8 : begin
			if(i4 == 0) nextState <= s9;
			else nextState <= s1;
		end
		s9 : begin
			if(i3 == 1) nextState <= s10;
			else nextState <= s1;
		end
		s10 : begin
			if(i4 == 1) nextState <= s11;
			else nextState <= s1;
		end
		s11 : begin
			if(i2 == 0) nextState <= s12;
			else nextState <= s1;
		end
		s12 : begin
			if(i1 == 0) nextState <= s13;
			else nextState <= s1;
		end
		s13 : begin
			if(i3 == 0) nextState <= s14;
			else nextState <= s1;
		end
		s14 : begin
		end
		endcase
	end
endmodule