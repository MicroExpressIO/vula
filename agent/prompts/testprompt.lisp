(atom 23.5)
(list 1 2 3)

(format t "hi test")
(print "haha here is another line ")

(defparameter *global* "global parameter")
(defvar *var* "by defvar")
(print *var*)
(print *global*) 


(defconstant PI 3.1415)

(defun circum-size(rad)
     "print the circumference of a circle"
    (* 2 PI rad)
)

(mapcar #'circum-size (list 5 10 20))

;(loop for x from 0 to 100 by 3 do  
    ;(print x)
;)

;;; define a macro
;(defmacro while (condition &body body)
    ;'(loop while ,condition do (progn ,@body)))

;(while )