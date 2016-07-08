module FSM(reset, clk, i1, i2);
	input reset, clk, i1, i2;
	parameter a=0, b=500, c=1000, d=1500, e=2000, f=2300, g=2800, h=3000, i=3300, j=3500, k=4000, l=4500;
	reg [1:0] state, nextState;

	always @(posedge clk) begin
		if(reset) begin
			state <= a;
			i1=0, i2=0;
		end
		else begin
			state <= nextState;
		end
	end

	always @(i1, i2) begin
		case(state)
		a : begin
			if(i1 == 1) nextState <= b;
		end
		b : begin
			if(i2 == 1) nextState <= c;
		end
		c : begin
			if(i1 == 0) nextState <= d;
		end
		d : begin
			if(i2 == 0) nextState <= e;
		end
		e : begin
			if(i1 == 1) nextState <= f;
		end
		f : begin
			if(i2 == 1) nextState <= g;
		end
		g : begin
			if(i1 == 0) nextState <= h;
		end
		h : begin
			if(i2 == 0) nextState <= i;
		end
		i : begin
			if(i2 == 1) nextState <= j;
		end
		j : begin
			if(i1 == 1) nextState <= k;
		end
		k : begin
			if(i1 == 0) nextState <= l;
		end
		endcase
	end
endmodule