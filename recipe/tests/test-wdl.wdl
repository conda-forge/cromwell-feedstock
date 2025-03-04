version 1.0

task HelloWorld {
    input {
        String helloLanguage = "English"
    }

    command <<<
        HELLO_LANGUAGE="~{helloLanguage}"
        if [ "$HELLO_LANGUAGE" = "English" ]; then
            echo "Hello, World!"
        else if [ "$HELLO_LANGUAGE" = "Nederlands" ]; then 
            echo "Hallo, Wereld!"
        else if [ "$HELLO_LANGUAGE" = "Deutsch" ]; then 
            echo "Guten Morgen, Guten Morgen, Guten Morgen, Sonnenschein!"
            echo "Diese Nacht blieb dir verborgen, doch du darfst nicht traurig sein."
        else 
            echo "Sorry, I don't speak $HELLO_LANGUAGE."
        fi 
        fi 
        fi
    >>>

    output {
        File result = stdout()
    }
}

task Concatenate {
    input {
        Array[File]+ files
    }
    command <<< 
        cat ~{sep=" " files} > result.txt
    >>>
    output {
        Array[String] result = read_lines("result.txt")
    }
}

workflow greetings {
    call HelloWorld as helloEnglish {}
    call HelloWorld as helloNederlands {
        input:
            helloLanguage="Nederlands"
    }
    call HelloWorld as helloFrancais {
        input:
            helloLanguage="Français"
    }
    call HelloWorld as helloDeutsch {
        input:
            helloLanguage = "Deutsch"
    }
    call Concatenate as cat {
        input:
            files = [
                helloEnglish.result, 
                helloNederlands.result, 
                helloFrancais.result, 
                helloDeutsch.result
            ]
    }

    output {
        Array[String] allHellos = cat.result
    }
}
