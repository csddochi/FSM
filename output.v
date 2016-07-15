module tb_and_test(reset, clk, i2, i1, i3, i4);
	input reset, clk, i2, i1, i3, i4;
	parameter s1 = 0, s2 = 200, s3 = 700, s4 = 900, s5 = 1300, s6 = 1800, s7 = 2300, s8 = 2800, s9 = 3100, s10 = 3400, s11 = 3600, s12 = 3800, s13 = 4100;
	reg[1:0] state, nextState;

	always @(posedge clk) begin
		if(reset) begin
			state <= s1;
			i2 = 0, i1 = 0, i3 = 0, i4 = 0;
		end
		else begin
			state <= nextState;
		end
	end

	always @(i2, i1, i3, i4) begin
		case(state)
		s1 : begin
			if(i3 == 1) nextState <= s2;
			else nextState <= s1;
		end
		s2 : begin
			if(i4 == 1 && i1 == 1) nextState <= s3;
			else if(i3 == 1) nextState <= s2;
			else nextState <= s1;
		end
		s3 : begin
			if(i3 == 0) nextState <= s4;
			else if(i4 == 1 && i1 == 1) nextState <= s3;
			else nextState <= s1;
		end
		s4 : begin
			if(i3 == 1 && i1 == 0) nextState <= s5;
			else if(i3 == 0) nextState <= s4;
			else nextState <= s1;
		end
		s5 : begin
			if(i2 == 1 && i4 == 0 && i1 == 0) nextState <= s6;
			else if(i3 == 1 && i1 == 0) nextState <= s5;
			else nextState <= s1;
		end
		s6 : begin
			if(i1 == 1) nextState <= s7;
			else if(i2 == 1 && i4 == 0 && i1 == 0) nextState <= s6;
			else nextState <= s1;
		end
		s7 : begin
			if(i4 == 1) nextState <= s8;
			else if(i1 == 1) nextState <= s7;
			else nextState <= s1;
		end
		s8 : begin
			if(i3 == 0 && i4 == 0) nextState <= s9;
			else if(i4 == 1) nextState <= s8;
			else nextState <= s1;
		end
		s9 : begin
			if(i4 == 1 && i1 == 0) nextState <= s10;
			else if(i3 == 0 && i4 == 0) nextState <= s9;
			else nextState <= s1;
		end
		s10 : begin
			if(i2 == 0 && i3 == 1) nextState <= s11;
			else if(i4 == 1 && i1 == 0) nextState <= s10;
			else nextState <= s1;
		end
		s11 : begin
			if(i4 == 0 && i1 == 1) nextState <= s12;
			else if(i2 == 0 && i3 == 1) nextState <= s11;
			else nextState <= s1;
		end
		s12 : begin
			if(i3 == 0) nextState <= s13;
			else if(i4 == 0 && i1 == 1) nextState <= s12;
			else nextState <= s1;
		end
		s13 : begin
		end
		endcase
	end
endmodule