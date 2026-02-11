dist = table;
elements= 10;
X= cell(elements,1);
for n = 1:(elements)
    
    %X{n} = dist(n:(23-elements+n), n:(23-elements+n));
    X{n} = n:(23-elements+n);

end
all_combinations= combvec(X{:});
all_combinations = sort(all_combinations);

 comb_sizes = size(all_combinations);
 for n = 1: comb_sizes(2)
     if(size(unique( all_combinations(:,n))) < elements)
         all_combinations(:,n) =[];
     end
 end


