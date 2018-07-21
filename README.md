Remove commas within quotes
%s/".\{-}"/\=substitute(submatch(0), ',', '' , 'g')/g

Remove = signs
%s/=//g
