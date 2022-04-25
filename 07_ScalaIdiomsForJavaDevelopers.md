## 5 Scala Idioms for Java Developers

These are some Scala idioms that a Java Programmer can add to their toolbox

### 1. Scala's Option<> class: Programming without null
Consider the following Problem Statement: `Calculate the Future Value(FV) 
using interest rate(r), present value(PV), and time in years(n)`

The formula for this is 
```
FV = PV ( 1 + r ) ** n  
```
In Java, we could create a method/function like this:
```java
class InterestRates {
     Double calculateFutureValue(Integer presentValue, 
                                 Double interestRate, 
                                 Integer n) {
    
         return presentValue * Math.pow(1 + interestRate, n);
    }
}
```

A programmer has 2 considerations for `null` parameter values:
  - `null` parameter value can be used to signify "special"/"Out of Band" value. For e.g., we could rewrite the `calculateFutureValue` function, 
     so that when `interestRate` is `null`, the current market interest rate is used OR
  -  `null` can be treated as an unacceptable parameter value. It indicates that the parameter is essential to compute the value of
    the function. If the parameter is `null`, then the function will return null.
 
Conversely, when function is invoked, `null` parameter values can be used either :
   - to pass a "special" value. or
   - to indicate that the parameter value is not known

Whatever the intention of a `null` parameter value may be, the programmer needs to detect and handle `null` values in a special way.
Else, we will end up with a NPE.
 
This results in multiple `null` checks(`if` statements) spread over our function definition.
Consider the function below:
```java
class InterestRates {
    Double calculateTaxPayable(Integer presentValue, Double interestRate, Integer n, Double taxRate) {

        if(presentValue != null && interestRate != null && n != null && taxRate != null) {
            Double futureValue = calculateFutureValue(presentValue, interestRate, n);
            if(futureValue != null)
                Double taxPayable = futureValue * taxRate;
                return taxPayable;
        } 
        return null;
    }
}
```
First, the function verifies that none of its parameters are nulls.

Then it invokes `calculateFutureValue`

Then again, it has to check if the return value is null. 

What if we could avoid all this `null` checking? 
In Scala, we use the the `Option` monad to handle null/unknown values. A similar class called `Optional` is available in Java. 

With `Optional`, we can avoid `null` checks and also combine(or chain) the parameters without having to worry about `null` values.

Let us see how we can rewrite the same method using `Optional`:

```java
class InterestRates {
    Optional<Double> calculateFutureValue(Optional<Integer> presentValue, 
                                 Optional<Double> interestRate, 
                                 Optional<Integer> n) {

            return presentValue.flatMap(pv -> 
                           interestRate.flatMap(r -> 
                                        n.flatMap( nv -> Optional.of(pv * Math.pow(1 + r, nv)))));
    }
}
```

The caller of the function can invoke this function with 
```
    Optional<Double> fv = calculateFutureValue(Optional.of(1), Optional.of(2.0), Optional.of(3));
```

If some parameter values are not available(or unknown or null), then we need to use a special type of `Optional` 

```
    Optional<Double> fv = futureValue(Optional.empty(), Optional.of(2.0), Optional.of(3))
```

This eliminates all the ```if(x == null)``` checks in our code and make it more readable.

However, a caller could invoke the function with `null` which will still result in a `NullPointerException`.

```scala
   futureValue(null, null, null)
```
So what is the problem that is being solved with `Optional`?

Without `Optional` , if we do not know the value of a parameter, we use `null`. 
Then we are forced to use `null` checks in the function body.

With `Optional`, if we do not know the value of a parameter, we us `Optional.empty`.  And we get to skip all `null` checks
in function body.
If one of the parameters is `Optionsl.empty`, the chain of `flatMaps` will also return `Optional.empty` without 
us having to put in any null checks or `if` conditions.

The return value of the function invocation is an `Optional<Double>`. 
This can either be passed to another function or the actual `Double` value can be extracted 
using `get` or `orElse` 

```java
class InterestRates {

    Optional<Double> calculateTaxPayable(Optional<Integer> presentValue, 
                                        Optional<Double> interestRate, 
                                        Optional<Integer> n, 
                                        Optional<Double> taxRate) {

                 // no need to `null` check the parameters
                 Optional<Double> futureValue = presentValue.flatMap(pv -> 
                                    interestRate.flatmap(i -> 
                                                    n.flatMap(nv-> taxRate.flatMap(t -> ))));
                  
                 // ... no need to `null` check the return values
                 Optional<Double> tax = futureValue.flatMap(fv -> taxRate.flatMap(t -> Optional.of(fv * t)));
                 return tax;
    }

   // ...or...

   // non functional style...
   Double calculateTaxPayable_NON_FUNCTIONAL_STYLE(Optional<Integer> presentValue, 
                                        Optional<Double> interestRate, 
                                        Optional<Integer> n, 
                                        Double taxRate) {
                 Optional<Double> futureValue = presentValue.flatMap(pv -> 
                                    interestRate.flatmap(i -> 
                                                    n.flatMap(nv-> taxRate.flatMap(t -> ))));
                  
                 Optional<Double> tax = futureValue.getOrElse(0) * taxRate ;
                 return tax;
    }
}
```
We have eliminated `null` checking, facilitated function chaining and also and made our code more readable.

There are some drawbacks to consider:

    - 1.  Every `Optional<>` is a additional object that adds to the memory cost 
    - 2.  We can only return success `Optional<Value>` or failure `Optional.empty`. 

It would have been great if we could return additional info for the failure(see scala.util.Either/Left/Right)


### 2. Scala's case classes:Quick Data(DTO) Classes

In Java, when we define POJOs, we are forced to define a large amount of boilerplate code.
 This includes:
  - getters and setters
  - hashCode() and equals()
  - toString()
  - factories and/or builders
  
Although this code is autogenerated by most IDEs, it would still be nice to avoid this manual step.

Also, when we add or remove a field from an existing auto-generated class, 
we have to make sure not to break the autogenerated methods.

Scala has "case" classes. These classes help eliminate a lot of boilerplate code.
When we define a "case" class, we get the  all the above methods for free.
The Scala syntax is quite straightforward:
```scala
case class MyScalaPojo(var name:String, var age:Int, var address:Array[String]);
val myPojo = MyScalaPojo("John", 33, Array("House No 10", "Thailand"))
myPojo.name = "James";
```

Java 14 has record classes which provide similar functionality. 
In Java versions lower than 14, we can achieve similar economy of code using the Lombok Library. 

To add Lombok to our project, we can add the following
dependency to the pom file.
```xml
<dependencies>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.18.20</version> <!-- check for later versions -->
        <scope>provided</scope>
    </dependency>
</dependencies>
```

Also, do not forget to add the [Lombok Plugin for your IDE](https://projectlombok.org/setup/overview).

Let us see how boilerplate code is reduced with Lombok.
 
 Lombok introduces multiple annotations that automate a lot of the boilerplate code. 
 - @Getter and @Setter will auto generate getters and setters for all fields
     - @Getter and @Setter can also be applied at field level to restrict getters and setters to specific fields
 - @EqualsAndHashCode and @ToString will generate the synonymous methods. 
     - @ToString.Exclude will exclude a field from toString. Same with @EqualsAndHashCode.Exclude
 - @Builder will generate Factory methods
 - @Singleton will allow creation of a Singleton
  
```java

import lombok.*;

@Getter @Setter
@EqualsAndHashCode 
@ToString(includeFieldNames = true) 
@Builder(toBuilder = true)
class Data {

    @Getter @Setter // this is redundant, since we have used @Getter and @Setter at class level
    private String name;

    @Getter @Setter @ToString.Exclude @EqualsAndHashCode.Exclude
    private String[] address;

}
```

We can then invoke the `getters`, `setters` and other methods as usual:

```java

public class Main {

    public static void main(String[] args) {

        Data data = Data.builder().
                    name("John"). // auto generated
                    address(new String[]{"New Delhi", "India"}).//auto generated
                    build(); // auto generated Builder
        data.setName("Jane"); // auto generated Setter
        data.setAddress(new String[]{"Mumbai", "India"}); //auto generated Setter
        System.out.println(data.toString()); //auto generated toString
    }
}

```

Lombok also provides shortcuts that combine multiple annotations:

    - @lombok.Data will generate Getters, Setters, toString, and hashCode
    - @lombok.Value will generate all above methods except Setters
    
Using the `lombok.Data` annotation:
```java
@lombok.Data
class Data { 
    private String name;
    private String[] address;
}
```

Using the `lombok.Value` annotation
```java
@lombok.Value // @ToString, @EqualsAndHashCode, @Getter
class V { 
    private String name;
    private String[] address;
}
```

### 3. Scala's var and val: Less Boilerplate code with Type Inference 

In Scala, we do not have to define the `type` of a variable. Scala is able to infer the type. 
```scala
    var name = "John Doe"
    var age = 33
```
We can rely on the smartness of the compiler to make our code more readable.
Developers can still specify the type if they want though.
```scala
    var name:String = "John Doe"
    var age:Int = 33

    name = "John James Doe"
    age = 44
```
Thanks to Lombok, we can now pretend that the Java Compiler is as smart as Scala.

```java
    import lombok.*;
    var javaName = "John";
    var javaAge = 33;
    var javaObject = new StringBuilder("")
```

Lombok also adds the "val" `"keyword"` to Java. This makes variables immutable. 

```java
    val javaName = "John";
    javaName = "James";// Not allowed 
```

Lombok uses Annotation Processing to make them available in Java.
Note that `var` has been introduced as a keywork in Java 10.

### 4. Scala's predefined functional Interfaces: Refactor and Reuse Lambdas 

While programming with streams, we frequently use `.map` and `.filter` to modify collection streams.

Consider this code snippet:
```java
    firstIntegerList.map(i -> i + 1).filter(i -> i%2 == 0)
    secondIntegerList.map(i -> i + 1).filter(i -> i%2 == 0)
``` 
We are duplicating the lambda function code in `filter` and `map` invocations.
We could factor out the code using one of the predefined functional interfaces like so

```java
   Function<Integer, Integer> incrementer = i -> i + 1;
   Predicate<Integer> evenChecker = i -> i % 2 == 0;
```
Then we can use the same function objects for both the streams
```java
    firstIntegerList.map(incrementer).filter(evenChecker);
    secondIntegerList.map(incrementer).filter(evenChecker);
```

In Java, we have predefined Functional Interfaces defined in java.util.function

| Interface | Description                                         |
|-----------|-----------------------------------------------------|
| Supplier  | A function that takes in nothing and produces data  |
| Consumer  | A function that takes in data and producing nothing |
| Function  | A function that takes in data and produces data     |
| Predicate | A function that takes in data and returns a boolean |

### 5. Scala's collection classes: Quickly creating collections

In Scala, we can quickly create a List with  `val newList = List(1, 2, 3)`
The Java equivalent would be 
```java
    List<Integer> newList = ArrayList();
    newList.add(1);
    newList.add(2);
    newList.add(3);
```

[Google's Guava library](https://github.com/google/guava/wiki) allows us to use Scala-like syntax to create collections.
To add Guava to your project, add the following to your pom.xml.
```
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>31.0.1-jre</version> <!-- Check for later versions -->
</dependency>
```

Then, use the Factory methods in Guava classes to create collections:

```
    List<Integer> newList = ImmutableList.of(1, 2, 3)
    Map<Integer, String> newMap = ImmutalbeMap.of(1,"hello", 2, "bye")
```

Java programmers can use these 5 tips to add some Scala flavour to their code. 