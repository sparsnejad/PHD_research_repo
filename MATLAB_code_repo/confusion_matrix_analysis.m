function [ output_args ] = confusion_matrix_analysis( input_matrix )
%CONFUSION_MATRIX_ANALYSIS Summary of this function goes here
%   Detailed explanation goes here
[input_size, temp] = size(input_matrix);
input_matrix(input_matrix==0.5) = 0;
target=0;
bad_apples = 0;
for row = 1:input_size
    for col= 1:input_size
        if(input_matrix(row, col) == 0.5)
            bad_apples = bad_apples +1;
        elseif(row == col)
            target= target + 1 - input_matrix(row, col);
        else
            target= target + input_matrix(row, col);
        end
    end
end
output_args= target/(input_size*input_size-bad_apples);
clearvars target input_size row col temp bad_apples;


end

