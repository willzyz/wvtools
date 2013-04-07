    function writeTextFile(fileName,fileInput,opt)
    % writeTextFile(fileName,fileInput,options)
    % Prints a matrix to text file, a cell array of strings, or a
    % cell array of cells of strings
    % opt.writeFlag =
    %       'a'     open or create file for writing; append data to
    %       end of file
    %       'r+'    open (do not create) file for reading and
    %       writing
    %       'w+'    open or create file for reading and writing;
    %       discard
    %               existing contents
    %       'a+'    (default) open or create file for reading and
    %       writing; append data
    %               to end of file
    %       'W'     open file for writing without automatic
    %       flushing
    %       'A'     open file for appending without automatic
    %       flushing
    % opt.separator =
    %       '\n' (default) or ';' or ' ' etc.
    % richard _at_ socher .org

    if ~exist('opt','var') || (exist('opt','var') && ~isfield(opt, ...
                                                          'writeFlag'))
        opt.writeFlag='a+';
    end

    if ~exist('opt','var') || (exist('opt','var') && ~isfield(opt, ...
                                                          'separator'))
        opt.separator='\n';
    end
    if isnumeric(fileInput)
        % Write the matrix to file with separated
        fid = fopen(fileName, opt.writeFlag);
        fprintf(fid, [repmat(['%g' opt.separator], 1, size(fileInput,2)-1) ...
                      '%g\n'],fileInput);
        fclose(fid);

    elseif iscell(fileInput{1})
        fid = fopen(fileName, opt.writeFlag);
        for s = 1:length(fileInput)
            for w = 1:length(fileInput{s})
                if ischar(fileInput{s})
                    fprintf(fid, ['%s' opt.separator], ...
                            fileInput{s}{w});
                else
                    fprintf(fid, ['%s' opt.separator], ...
                            num2str(fileInput{s}{w}));
                end
            end
            fprintf(fid, '\n');
        end
        fclose(fid);
    else

        fid = fopen(fileName, opt.writeFlag);
        for s = 1:length(fileInput)
            if ischar(fileInput{s})
                fprintf(fid, ['%s' opt.separator], fileInput{s});
            else
                fprintf(fid, ['%s' opt.separator], ...
                        num2str(fileInput{s}));
            end
        end
        if ~strcmp(opt.separator,'\n')
            fprintf(fid, '\n');
        end
        fclose(fid);
    end
