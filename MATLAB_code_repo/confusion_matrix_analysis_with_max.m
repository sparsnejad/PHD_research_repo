function [ output_args, max ] = confusion_matrix_analysis( input_matrix )
%CONFUSION_MATRIX_ANALYSIS Summary of this function goes here
%   Detailed explanation goes here
[input_size, temp] = size(input_matrix);
target=0;
maxi= 0;
for row = 1:input_size
    for col= 1:input_size
        if(row == col)
            target= target + 1 - input_matrix(row, col);
            %do noting
        else
            target= target + input_matrix(row, col);
			if (maxi <input_matrix(row, col))
				maxi = input_matrix(row, col);
			end
        end
    end
end
output_args= target/(input_size*input_size);
max= maxi;
clearvars target input_size row col temp mini;


end

