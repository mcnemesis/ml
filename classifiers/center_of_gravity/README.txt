This classifier learns using a simple technique:

1. Given labelled data of the form D[x,y,w,label]
    
    where for a record d[x,y,w,label], x,y and w are real numbers denoting the location in a catesian space, and w denoting a weight
    of the record (but this could also just be location in 3D cartesian space), and label is the class of the record.

2. For each distinct label l, find all records belonging to that group (d[x,y,w,label==l]) and group them together under group Dl

    Dl = {d | d[x,y,w,label == l] }

3. Learning: For a group Dl, learn it's center of gravity cg(Dl)

    cg(Dl) = { c[cg(x),cg(y),cg(w),cg(l)] | 
        cg(x) = sum(d(w)*d(x)) / length(Dl) 
        cg(y) = sum(d(w)*d(y)) / length(Dl) 
        cg(w) = sum(d(w)) / length(Dl) 
        cg(l) = Dl(l)
    }

    Note: the learning here is in batch mode -- possible performance penalty for small, new observations

7. To classify / label a new item n[x,y,w,?]:
    1. From the list of learned Groups, find one for which the new element deviates the least from the group's center of gravity
        (taking into account the item's weight). 
    2. Assign that group's label to the new item.


    n(l) = {cg(L) : distance(n[x,y,w] , cg(DL)) = min(sqr_distance(n[x,y,w] , cg(Dl))) for all Dl }

    where

    sqr_distance(n[x,y,w],cg(Dl)) = { ((n(x)*n(w))-(cg(x)*cg(w)))^2 + ((n(y)*n(w))-(cg(y)*cg(w)))^2 }
