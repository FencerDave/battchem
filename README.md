# Project BattChem: 
### Finding the Balance between Empirical data and Electrochemical fundamentals in Battery Engineering
-----------------------------------------------------------
The field of Battery Engineering is beset on all sides by poor data practices, and a lack in transparency regarding designs and models. State-of-the-Art battery models in industry are tightly controlled secrets, even though we all know the best in class are still prone to failure! On the other hand, Physics-based models from academia are (in my experience) subject to every individual researchers' personal preference of fundamentals and without clear explaination it's very easy to misinterperet (some would say impossible to avoid!). 

One of the most trustworthy tools I've found is the [BatPaC (Battery Performance and Cost) model from Argonne National Laboratory](https://www.anl.gov/tcp/batpac-battery-manufacturing-cost-estimation), and it makes sense that a National Lab would have the good-faith effort and opportunity to share a User-Focused model to find the balance between empirically useful modeling and good battery fundamentals. Unfortunately they accomplish this in part by only focusing on commercially relevent and studied chemistries, and don't have the flexibility to account for Aqueous batteries, Redox Flow Cells, etcetera. In additon, the BatPaC model is excel-heavy and so can be slow when trying to do more advanced work such as modeling cycling data. 

I'm hoping to take a "No-BS" approach to battery modeling, inspired by the BatPaC/Argonne team, by starting from a few electrochemical fundamentals but allowing a user to modify or fit those parameters to create the model which fits their data and build design. 

