library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.std_logic_arith.all;

entity sevensegment_decoder is
	port(
		bcd : in std_logic_vector(7 downto 0);
		clk: in std_logic;
		segment7 : out std_logic_vector(6 downto 0)
	);
end sevensegment_decoder;

architecture behaviour of sevensegment_decoder is
		signal digit : std_logic_vector(3 downto 0);
		begin
			process(bcd)
				begin
					if rising_edge(clk) then
					digit(3 downto 0) <= bcd(3 downto 0);
					case digit is
						when "0000" => segment7 <= "0111111";--0
						when "0001" => segment7 <= "0000110";--1
						when "0010" => segment7 <= "1011011";--2
						when "0011" => segment7 <= "1001111";--3
						when "0100" => segment7 <= "1100110";--4
						when "0101" => segment7 <= "1101101";--5
						when "0110" => segment7 <= "1111101";--6
						when "0111" => segment7 <= "0000111";--7
						when "1000" => segment7 <= "1111111";--8
						when "1001" => segment7 <= "1101111";--9
						
						when others => segment7 <= "0000000"; 
					end case;
					end if;
			end process;
end behaviour;			
	